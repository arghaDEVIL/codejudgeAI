import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { roomsAPI, problemsAPI, testcasesAPI } from '../utils/api';
import { useWebSocket } from '../hooks/useWebSocket';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { ThemeToggle } from '@/components/theme-toggle';
import {
    Users,
    MessageSquare,
    FileText,
    Play,
    CheckSquare,
    LogOut,
    Code2,
    X,
    Send,
    Loader2,
    AlertCircle,
    User
} from 'lucide-react';

const CollaborativeRoom = () => {
    const { roomCode } = useParams();
    const navigate = useNavigate();
    const editorRef = useRef(null);
    const chatMessagesRef = useRef(null);

    // Room state
    const [room, setRoom] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [language, setLanguage] = useState('python');
    const [code, setCode] = useState(`# Python Solution
def solution():
    """
    Write your solution here
    """
    pass

if __name__ == "__main__":
    solution()
`);
    const [problem, setProblem] = useState(null);
    const [testcases, setTestcases] = useState([]);
    const [isJoined, setIsJoined] = useState(false);

    // UI state
    const [showChat, setShowChat] = useState(true);
    const [showParticipants, setShowParticipants] = useState(true);
    const [showProblem, setShowProblem] = useState(true);
    const [chatMessage, setChatMessage] = useState('');
    const [remoteCursors, setRemoteCursors] = useState({});
    const [showOutput, setShowOutput] = useState(false);
    const [output, setOutput] = useState(null);
    const [isRunning, setIsRunning] = useState(false);
    const [isRunningTests, setIsRunningTests] = useState(false);
    const [testResults, setTestResults] = useState(null);

    // WebSocket connection
    const {
        connected,
        connecting,
        error: wsError,
        messages,
        participants,
        roomState,
        sendCodeChange,
        sendChatMessage,
        disconnect,
    } = useWebSocket(roomCode, isJoined);

    // Load room details
    useEffect(() => {
        loadRoom();
    }, [roomCode]);

    // Update code from room state
    useEffect(() => {
        if (roomState?.current_code) {
            setCode(roomState.current_code);
        }
        if (roomState?.current_language) {
            setLanguage(roomState.current_language);
        }
    }, [roomState]);

    // Listen for code updates from other users
    useEffect(() => {
        const handleCodeUpdate = (event) => {
            const { code: newCode, language: newLang } = event.detail;
            setCode(newCode);
            if (newLang) setLanguage(newLang);
        };

        const handleCursorUpdate = (event) => {
            const { user_id, user_name, cursor_color, position } = event.detail;
            setRemoteCursors(prev => ({
                ...prev,
                [user_id]: {
                    user_name,
                    cursor_color,
                    position,
                    timestamp: Date.now()
                }
            }));
        };

        const handleCodeExecution = (event) => {
            const { user_id, user_name, result } = event.detail;
            setShowOutput(true);
            setOutput({
                ...result,
                executedBy: user_name,
                executedByUserId: user_id
            });
            setTestResults(null);
        };

        const handleTestResults = (event) => {
            const { user_id, user_name, results } = event.detail;
            setShowOutput(true);
            setTestResults({
                ...results,
                executedBy: user_name,
                executedByUserId: user_id
            });
            setOutput(null);
        };

        window.addEventListener('code_update', handleCodeUpdate);
        window.addEventListener('cursor_update', handleCursorUpdate);
        window.addEventListener('code_execution', handleCodeExecution);
        window.addEventListener('test_results', handleTestResults);

        return () => {
            window.removeEventListener('code_update', handleCodeUpdate);
            window.removeEventListener('cursor_update', handleCursorUpdate);
            window.removeEventListener('code_execution', handleCodeExecution);
            window.removeEventListener('test_results', handleTestResults);
        };
    }, []);

    // Auto-scroll chat to bottom
    useEffect(() => {
        if (chatMessagesRef.current) {
            chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
        }
    }, [messages]);

    const loadRoom = async () => {
        setLoading(true);
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            const displayName = user.name || user.email || 'Anonymous';

            try {
                const joinResponse = await roomsAPI.join(roomCode, { display_name: displayName });
                setRoom(joinResponse.data.room);
                if (joinResponse.data.room.current_code) {
                    setCode(joinResponse.data.room.current_code);
                }
                if (joinResponse.data.room.current_language) {
                    setLanguage(joinResponse.data.room.current_language);
                }

                if (joinResponse.data.room.problem_id) {
                    await loadProblem(joinResponse.data.room.problem_id);
                }

                setIsJoined(true);
            } catch (joinErr) {
                if (joinErr.response?.status === 400) {
                    const response = await roomsAPI.getByCode(roomCode);
                    setRoom(response.data);
                    if (response.data.current_code) {
                        setCode(response.data.current_code);
                    }
                    if (response.data.current_language) {
                        setLanguage(response.data.current_language);
                    }

                    if (response.data.problem_id) {
                        await loadProblem(response.data.problem_id);
                    }

                    setIsJoined(true);
                } else {
                    throw joinErr;
                }
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to load room');
        } finally {
            setLoading(false);
        }
    };

    const loadProblem = async (problemId) => {
        try {
            const [problemRes, testcasesRes] = await Promise.all([
                problemsAPI.getById(problemId),
                testcasesAPI.getByProblem(problemId)
            ]);
            setProblem(problemRes.data);
            setTestcases(testcasesRes.data);
        } catch (err) {
            console.error('Failed to load problem:', err);
        }
    };

    const handleEditorDidMount = (editor) => {
        editorRef.current = editor;
    };

    const handleCodeChange = (value) => {
        setCode(value || '');
        if (handleCodeChange.timeout) {
            clearTimeout(handleCodeChange.timeout);
        }
        handleCodeChange.timeout = setTimeout(() => {
            sendCodeChange(value || '', language);
        }, 500);
    };

    const handleLanguageChange = (newLang) => {
        const template = getLanguageTemplate(newLang);
        setLanguage(newLang);
        setCode(template);
        sendCodeChange(template, newLang);
    };

    const getLanguageTemplate = (lang) => {
        const templates = {
            python: `# Python Solution
def solution():
    """
    Write your solution here
    """
    pass

if __name__ == "__main__":
    solution()
`,
            javascript: `// JavaScript Solution
function solution() {
    /**
     * Write your solution here
     */
    
}

console.log(solution());
`,
            typescript: `// TypeScript Solution
function solution(): any {
    /**
     * Write your solution here
     */
    
}

console.log(solution());
`,
            java: `// Java Solution
public class Solution {
    public static void main(String[] args) {
        Solution sol = new Solution();
        System.out.println(sol.solution());
    }
    
    public Object solution() {
        return null;
    }
}
`,
            cpp: `// C++ Solution
#include <iostream>
using namespace std;

class Solution {
public:
    void solution() {
        
    }
};

int main() {
    Solution sol;
    sol.solution();
    return 0;
}
`,
            c: `// C Solution
#include <stdio.h>

void solution() {
    
}

int main() {
    solution();
    return 0;
}
`,
            csharp: `// C# Solution
using System;

public class Solution {
    public static void Main(string[] args) {
        Solution sol = new Solution();
        Console.WriteLine(sol.SolutionMethod());
    }
    
    public object SolutionMethod() {
        return null;
    }
}
`,
            go: `// Go Solution
package main

import "fmt"

func solution() {
    
}

func main() {
    solution()
}
`,
            rust: `// Rust Solution
fn solution() {
    
}

fn main() {
    solution();
}
`
        };

        return templates[lang] || `// Start coding here...\n`;
    };

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (!chatMessage.trim()) return;

        sendChatMessage(chatMessage);
        setChatMessage('');
    };

    const handleRunCode = async () => {
        setIsRunning(true);
        setOutput(null);
        setTestResults(null);
        setShowOutput(true);

        try {
            const response = await roomsAPI.runCode(roomCode, {
                code,
                language
            });

            setOutput(response.data);
        } catch (err) {
            setOutput({
                success: false,
                error: err.response?.data?.detail || 'Failed to execute code',
                output: '',
                execution_time: 0
            });
        } finally {
            setIsRunning(false);
        }
    };

    const handleRunTests = async () => {
        if (!problem) return;

        setIsRunningTests(true);
        setOutput(null);
        setTestResults(null);
        setShowOutput(true);

        try {
            const response = await roomsAPI.runTests(roomCode, {
                code,
                language
            });

            setTestResults(response.data);
        } catch (err) {
            setTestResults({
                passed: 0,
                total: testcases.length,
                error: err.response?.data?.detail || 'Failed to run tests',
                results: []
            });
        } finally {
            setIsRunningTests(false);
        }
    };

    const handleLeaveRoom = async () => {
        if (window.confirm('Are you sure you want to leave this room?')) {
            try {
                await roomsAPI.leave(roomCode);
                disconnect();
                navigate('/rooms');
            } catch (err) {
                console.error('Failed to leave room:', err);
                disconnect();
                navigate('/rooms');
            }
        }
    };

    const getParticipantColor = (userId) => {
        const participant = participants.find(p => p.user_id === userId);
        return participant?.cursor_color || '#667eea';
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-background">
                <Card className="w-96">
                    <CardContent className="flex flex-col items-center gap-4 pt-6">
                        <Loader2 className="h-12 w-12 animate-spin text-primary" />
                        <p className="text-muted-foreground">Loading room...</p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-screen bg-background">
                <Card className="w-96 border-destructive">
                    <CardContent className="flex flex-col items-center gap-4 pt-6">
                        <AlertCircle className="h-16 w-16 text-destructive" />
                        <h2 className="text-xl font-semibold text-destructive">Failed to Load Room</h2>
                        <p className="text-muted-foreground text-center">{error}</p>
                        <Button onClick={() => navigate('/rooms')}>
                            Back to Lobby
                        </Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-screen bg-background">
            {/* Header */}
            <div className="border-b bg-card">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4 flex-1">
                        <h1 className="text-xl font-semibold">{room?.title || 'Collaborative Room'}</h1>
                        <Badge variant="secondary" className="font-mono font-bold tracking-wider">
                            {roomCode}
                        </Badge>
                        <div className="ml-auto">
                            {connecting && (
                                <Badge variant="outline" className="gap-2">
                                    <Loader2 className="h-3 w-3 animate-spin" />
                                    Connecting...
                                </Badge>
                            )}
                            {connected && (
                                <Badge variant="outline" className="gap-2 border-green-500 text-green-500">
                                    <span className="h-2 w-2 rounded-full bg-green-500" />
                                    Connected
                                </Badge>
                            )}
                            {wsError && (
                                <Badge variant="outline" className="gap-2 border-destructive text-destructive">
                                    <span className="h-2 w-2 rounded-full bg-destructive" />
                                    Disconnected
                                </Badge>
                            )}
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <ThemeToggle />

                        <Button variant="outline" size="sm" onClick={() => navigate('/dashboard')}>
                            <User className="h-4 w-4 mr-2" />
                            <span className="hidden sm:inline">Dashboard</span>
                        </Button>

                        {problem && (
                            <Button
                                variant={showProblem ? "default" : "outline"}
                                size="sm"
                                onClick={() => setShowProblem(!showProblem)}
                            >
                                <FileText className="h-4 w-4" />
                            </Button>
                        )}

                        <Button
                            variant={showParticipants ? "default" : "outline"}
                            size="sm"
                            onClick={() => setShowParticipants(!showParticipants)}
                            className="relative"
                        >
                            <Users className="h-4 w-4" />
                            <Badge variant="destructive" className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs">
                                {participants.length}
                            </Badge>
                        </Button>

                        <Button
                            variant={showChat ? "default" : "outline"}
                            size="sm"
                            onClick={() => setShowChat(!showChat)}
                            className="relative"
                        >
                            <MessageSquare className="h-4 w-4" />
                            {messages.filter(m => m.type === 'chat').length > 0 && (
                                <Badge variant="destructive" className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs">
                                    {messages.filter(m => m.type === 'chat').length}
                                </Badge>
                            )}
                        </Button>

                        <Button
                            variant="destructive"
                            size="sm"
                            onClick={handleLeaveRoom}
                        >
                            <LogOut className="h-4 w-4 mr-2" />
                            Leave
                        </Button>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex flex-1 overflow-hidden">
                {/* Problem Panel */}
                {problem && showProblem && (
                    <Card className="w-[350px] rounded-none border-y-0 border-l-0">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <FileText className="h-5 w-5" />
                                Problem
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0">
                            <ScrollArea className="h-[calc(100vh-180px)]">
                                <div className="px-6 pb-6">
                                    <div className="flex items-start justify-between mb-4 pb-4 border-b">
                                        <h2 className="text-lg font-semibold flex-1">{problem.title}</h2>
                                        <Badge
                                            variant={
                                                problem.difficulty.toLowerCase() === 'easy' ? 'default' :
                                                    problem.difficulty.toLowerCase() === 'medium' ? 'secondary' :
                                                        'destructive'
                                            }
                                        >
                                            {problem.difficulty}
                                        </Badge>
                                    </div>

                                    <div className="space-y-4">
                                        <div>
                                            <h4 className="text-sm font-semibold text-primary mb-2">Problem Statement</h4>
                                            <p className="text-sm text-muted-foreground whitespace-pre-wrap leading-relaxed">
                                                {problem.statement}
                                            </p>
                                        </div>

                                        <Separator />

                                        <div className="text-sm text-muted-foreground">
                                            📊 Test Cases: {testcases.length}
                                        </div>
                                    </div>
                                </div>
                            </ScrollArea>
                        </CardContent>
                    </Card>
                )}

                {/* Participants Sidebar */}
                {showParticipants && (
                    <Card className="w-[280px] rounded-none border-y-0 border-l-0">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Users className="h-5 w-5" />
                                Participants ({participants.length})
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0">
                            <ScrollArea className="h-[calc(100vh-180px)]">
                                <div className="px-4 pb-4 space-y-2">
                                    {participants.map((participant) => (
                                        <div
                                            key={`${participant.user_id}-${participant.joined_at || Date.now()}`}
                                            className="flex items-center gap-3 p-3 rounded-lg hover:bg-accent transition-colors"
                                        >
                                            <div
                                                className="h-10 w-10 rounded-full flex items-center justify-center text-white font-bold shadow-md"
                                                style={{ background: participant.cursor_color }}
                                            >
                                                {participant.display_name.charAt(0).toUpperCase()}
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center gap-2">
                                                    <span className="font-semibold text-sm truncate">
                                                        {participant.display_name}
                                                    </span>
                                                    {participant.role === 'host' && (
                                                        <span className="text-sm">👑</span>
                                                    )}
                                                </div>
                                                <div className="text-xs text-muted-foreground">
                                                    {participant.is_active ? '🟢 Active' : '⚫ Inactive'}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </ScrollArea>
                        </CardContent>
                    </Card>
                )}

                {/* Editor Area */}
                <div className="flex-1 flex flex-col overflow-hidden">
                    <div className="border-b bg-card px-6 py-3 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <Code2 className="h-5 w-5 text-primary" />
                                <Select value={language} onValueChange={handleLanguageChange}>
                                    <SelectTrigger className="w-[180px]">
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="python">🐍 Python</SelectItem>
                                        <SelectItem value="javascript">📜 JavaScript</SelectItem>
                                        <SelectItem value="typescript">📘 TypeScript</SelectItem>
                                        <SelectItem value="java">☕ Java</SelectItem>
                                        <SelectItem value="cpp">⚡ C++</SelectItem>
                                        <SelectItem value="c">🔧 C</SelectItem>
                                        <SelectItem value="csharp">💎 C#</SelectItem>
                                        <SelectItem value="go">🐹 Go</SelectItem>
                                        <SelectItem value="rust">🦀 Rust</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <Badge variant="outline" className="gap-2">
                                <Users className="h-3 w-3" />
                                Collaborative Mode
                            </Badge>
                        </div>

                        <div className="flex items-center gap-2">
                            <Button
                                onClick={handleRunCode}
                                disabled={isRunning || !connected}
                                size="sm"
                                className="bg-green-600 hover:bg-green-700"
                            >
                                {isRunning ? (
                                    <>
                                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        Running...
                                    </>
                                ) : (
                                    <>
                                        <Play className="h-4 w-4 mr-2" />
                                        Run Code
                                    </>
                                )}
                            </Button>

                            {problem && (
                                <Button
                                    onClick={handleRunTests}
                                    disabled={isRunningTests || !connected}
                                    size="sm"
                                >
                                    {isRunningTests ? (
                                        <>
                                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                            Testing...
                                        </>
                                    ) : (
                                        <>
                                            <CheckSquare className="h-4 w-4 mr-2" />
                                            Run Tests
                                        </>
                                    )}
                                </Button>
                            )}
                        </div>
                    </div>

                    <div className="flex-1 flex flex-col overflow-hidden">
                        <Editor
                            height={showOutput ? "60%" : "100%"}
                            language={language}
                            value={code}
                            onChange={handleCodeChange}
                            onMount={handleEditorDidMount}
                            theme="vs-dark"
                            options={{
                                minimap: { enabled: true },
                                fontSize: 14,
                                lineNumbers: 'on',
                                scrollBeyondLastLine: false,
                                automaticLayout: true,
                                tabSize: 4,
                                wordWrap: 'on',
                            }}
                        />

                        {showOutput && (
                            <Card className="h-[40%] rounded-none border-x-0 border-b-0">
                                <CardHeader className="py-3 px-4">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm flex items-center gap-2">
                                            <FileText className="h-4 w-4" />
                                            Output
                                            {output?.executedBy && (
                                                <span className="text-xs font-normal text-muted-foreground">
                                                    • Executed by {output.executedBy}
                                                </span>
                                            )}
                                        </CardTitle>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => setShowOutput(false)}
                                        >
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <ScrollArea className="h-[calc(40vh-100px)]">
                                        <div className="px-4 pb-4 font-mono text-sm">
                                            {testResults ? (
                                                <div className="space-y-4">
                                                    <div className="flex items-center justify-between pb-4 border-b">
                                                        <h5 className="font-semibold">Test Results</h5>
                                                        <Badge
                                                            variant={testResults.all_passed ? "default" : "secondary"}
                                                            className={testResults.all_passed ? "bg-green-600" : ""}
                                                        >
                                                            {testResults.passed}/{testResults.total} tests passed
                                                            {testResults.all_passed && ' ✓'}
                                                        </Badge>
                                                    </div>

                                                    {testResults.error && (
                                                        <div className="p-3 bg-destructive/10 border border-destructive rounded-lg">
                                                            <strong className="text-destructive">Error:</strong>
                                                            <pre className="mt-2 text-destructive whitespace-pre-wrap">
                                                                {testResults.error}
                                                            </pre>
                                                        </div>
                                                    )}

                                                    {testResults.results && testResults.results.length > 0 && (
                                                        <div className="space-y-3">
                                                            {testResults.results.map((test, idx) => (
                                                                <Card
                                                                    key={idx}
                                                                    className={test.passed ? "border-green-500/50" : "border-destructive/50"}
                                                                >
                                                                    <CardHeader className="py-3 px-4">
                                                                        <div className="flex items-center justify-between">
                                                                            <div className="flex items-center gap-2">
                                                                                <span className="font-semibold">Test {test.test_number}</span>
                                                                                {test.is_sample && (
                                                                                    <Badge variant="outline" className="text-xs">
                                                                                        Sample
                                                                                    </Badge>
                                                                                )}
                                                                            </div>
                                                                            <Badge
                                                                                variant={test.passed ? "default" : "destructive"}
                                                                                className={test.passed ? "bg-green-600" : ""}
                                                                            >
                                                                                {test.passed ? '✓ Passed' : '✗ Failed'}
                                                                            </Badge>
                                                                        </div>
                                                                    </CardHeader>
                                                                    <CardContent className="px-4 pb-4 space-y-2">
                                                                        {test.error && (
                                                                            <div>
                                                                                <strong className="text-destructive text-xs">Error:</strong>
                                                                                <pre className="mt-1 p-2 bg-destructive/10 rounded text-destructive text-xs whitespace-pre-wrap">
                                                                                    {test.error}
                                                                                </pre>
                                                                            </div>
                                                                        )}

                                                                        {test.input !== null && (
                                                                            <div>
                                                                                <strong className="text-muted-foreground text-xs">Input:</strong>
                                                                                <pre className="mt-1 p-2 bg-muted rounded text-xs whitespace-pre-wrap">
                                                                                    {test.input}
                                                                                </pre>
                                                                            </div>
                                                                        )}

                                                                        {test.expected !== null && (
                                                                            <div>
                                                                                <strong className="text-muted-foreground text-xs">Expected:</strong>
                                                                                <pre className="mt-1 p-2 bg-muted rounded text-xs whitespace-pre-wrap">
                                                                                    {test.expected}
                                                                                </pre>
                                                                            </div>
                                                                        )}

                                                                        {test.actual !== null && (
                                                                            <div>
                                                                                <strong className="text-muted-foreground text-xs">Your Output:</strong>
                                                                                <pre className="mt-1 p-2 bg-muted rounded text-xs whitespace-pre-wrap">
                                                                                    {test.actual}
                                                                                </pre>
                                                                            </div>
                                                                        )}

                                                                        {!test.is_sample && test.passed && (
                                                                            <div className="text-green-600 text-xs italic">
                                                                                Hidden test case passed ✓
                                                                            </div>
                                                                        )}

                                                                        {test.execution_time !== undefined && (
                                                                            <div className="text-muted-foreground text-xs">
                                                                                Time: {test.execution_time.toFixed(3)}s
                                                                            </div>
                                                                        )}
                                                                    </CardContent>
                                                                </Card>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            ) : output ? (
                                                <div className="space-y-4">
                                                    {output.error && (
                                                        <div className="p-3 bg-destructive/10 border border-destructive rounded-lg">
                                                            <strong className="text-destructive">Error:</strong>
                                                            <pre className="mt-2 text-destructive whitespace-pre-wrap">
                                                                {output.error}
                                                            </pre>
                                                        </div>
                                                    )}
                                                    {output.output && (
                                                        <div className="p-3 bg-green-600/10 border border-green-600 rounded-lg">
                                                            <pre className="text-green-600 whitespace-pre-wrap">
                                                                {output.output}
                                                            </pre>
                                                        </div>
                                                    )}
                                                    {output.execution_time !== undefined && (
                                                        <div className="text-muted-foreground text-xs">
                                                            Execution time: {output.execution_time.toFixed(3)}s
                                                        </div>
                                                    )}
                                                </div>
                                            ) : (
                                                <div className="text-muted-foreground italic">
                                                    No output yet. Run your code to see results.
                                                </div>
                                            )}
                                        </div>
                                    </ScrollArea>
                                </CardContent>
                            </Card>
                        )}
                    </div>
                </div>

                {/* Chat Panel */}
                {showChat && (
                    <Card className="w-[320px] rounded-none border-y-0 border-r-0">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <MessageSquare className="h-5 w-5" />
                                Chat
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-0 flex flex-col h-[calc(100vh-180px)]">
                            <ScrollArea className="flex-1 px-4" ref={chatMessagesRef}>
                                {messages.length === 0 ? (
                                    <div className="flex items-center justify-center h-full text-center text-muted-foreground text-sm">
                                        <p>No messages yet. Start the conversation!</p>
                                    </div>
                                ) : (
                                    <div className="space-y-4 py-4">
                                        {messages.map((msg, index) => (
                                            <div key={`${msg.timestamp}-${index}`}>
                                                {msg.type === 'system' ? (
                                                    <div className="flex items-center justify-center gap-2 p-2 bg-primary/10 rounded-lg text-sm text-muted-foreground">
                                                        <span>ℹ️</span>
                                                        {msg.content}
                                                    </div>
                                                ) : (
                                                    <div className="flex gap-3">
                                                        <div
                                                            className="h-8 w-8 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-md"
                                                            style={{ background: getParticipantColor(msg.userId) }}
                                                        >
                                                            {msg.userName?.charAt(0).toUpperCase()}
                                                        </div>
                                                        <div className="flex-1 min-w-0">
                                                            <div className="flex items-center gap-2 mb-1">
                                                                <span className="font-semibold text-sm">
                                                                    {msg.userName}
                                                                </span>
                                                                <span className="text-xs text-muted-foreground">
                                                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                                                </span>
                                                            </div>
                                                            <div className="text-sm text-muted-foreground break-words">
                                                                {msg.content}
                                                            </div>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </ScrollArea>

                            <div className="border-t p-4">
                                <form onSubmit={handleSendMessage} className="flex gap-2">
                                    <Input
                                        type="text"
                                        value={chatMessage}
                                        onChange={(e) => setChatMessage(e.target.value)}
                                        placeholder="Type a message..."
                                        disabled={!connected}
                                        className="flex-1"
                                    />
                                    <Button
                                        type="submit"
                                        disabled={!connected || !chatMessage.trim()}
                                        size="sm"
                                    >
                                        <Send className="h-4 w-4" />
                                    </Button>
                                </form>
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
};

export default CollaborativeRoom;
