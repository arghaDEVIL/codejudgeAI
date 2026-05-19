import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { submissionsAPI, problemsAPI, aiFeedbackAPI, removeAuthToken } from "./utils/api";
import Editor from "@monaco-editor/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
    ArrowLeft,
    LogOut,
    Code,
    CheckCircle2,
    XCircle,
    Clock,
    Cpu,
    Loader2,
    Sparkles,
    RefreshCw,
    AlertCircle
} from "lucide-react";

export default function SubmissionDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [submission, setSubmission] = useState(null);
    const [problem, setProblem] = useState(null);
    const [aiFeedback, setAiFeedback] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingFeedback, setLoadingFeedback] = useState(false);

    useEffect(() => {
        loadSubmission();
    }, [id]);

    const loadSubmission = async () => {
        try {
            setLoading(true);
            const subRes = await submissionsAPI.getById(id);
            setSubmission(subRes.data);

            const probRes = await problemsAPI.getById(subRes.data.problem_id);
            setProblem(probRes.data);

            if (subRes.data.has_ai_feedback) {
                try {
                    const feedbackRes = await aiFeedbackAPI.getBySubmission(id);
                    setAiFeedback(feedbackRes.data);
                } catch (err) {
                    console.log("No AI feedback available yet");
                }
            }
        } catch (error) {
            console.error("Failed to load submission:", error);
        } finally {
            setLoading(false);
        }
    };

    const loadAIFeedback = async (regenerate = false) => {
        try {
            setLoadingFeedback(true);
            const res = regenerate
                ? await aiFeedbackAPI.regenerate(id)
                : await aiFeedbackAPI.getBySubmission(id);
            setAiFeedback(res.data);
        } catch (error) {
            console.error("Failed to load AI feedback:", error);
            alert("Failed to load AI feedback. Please try again.");
        } finally {
            setLoadingFeedback(false);
        }
    };

    const logout = () => {
        removeAuthToken();
        window.location.href = "/login";
    };

    const getStatusVariant = (status) => {
        if (status === "Accepted") return "default";
        if (status === "Wrong Answer") return "destructive";
        return "secondary";
    };

    const getStatusIcon = (status) => {
        if (status === "Accepted") return <CheckCircle2 className="w-5 h-5" />;
        if (status === "Wrong Answer") return <XCircle className="w-5 h-5" />;
        return <AlertCircle className="w-5 h-5" />;
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <Loader2 className="w-12 h-12 animate-spin text-primary" />
            </div>
        );
    }

    if (!submission) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <Card className="text-center p-8">
                    <CardHeader>
                        <CardTitle className="text-2xl">Submission Not Found</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Button onClick={() => navigate("/history")}>
                            Back to History
                        </Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b sticky top-0 z-50 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate("/history")}>
                            <ArrowLeft className="w-5 h-5" />
                        </Button>
                        <h1 className="text-2xl font-bold">Submission #{submission.id}</h1>
                    </div>

                    <Button variant="destructive" onClick={logout}>
                        <LogOut className="w-4 h-4 mr-2" />
                        <span className="hidden sm:inline">Logout</span>
                    </Button>
                </div>
            </header>

            <div className="max-w-7xl mx-auto p-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left Column */}
                    <div className="space-y-6">
                        {/* Problem Info */}
                        {problem && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-2xl">{problem.title}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap">
                                        {problem.statement}
                                    </p>
                                </CardContent>
                            </Card>
                        )}

                        {/* Status & Metrics */}
                        <Card>
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle>Status</CardTitle>
                                    <Badge variant={getStatusVariant(submission.status)} className="flex items-center gap-1">
                                        {getStatusIcon(submission.status)}
                                        {submission.status}
                                    </Badge>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {/* Metrics Grid */}
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                    <Card>
                                        <CardHeader className="p-4">
                                            <CardDescription className="text-xs">Score</CardDescription>
                                            <CardTitle className="text-2xl">
                                                {submission.score?.toFixed(1) || 0}/100
                                            </CardTitle>
                                        </CardHeader>
                                    </Card>
                                    <Card>
                                        <CardHeader className="p-4">
                                            <CardDescription className="text-xs">Tests</CardDescription>
                                            <CardTitle className="text-2xl">
                                                {submission.testcase_results.filter(r => r.status === "Passed").length}/
                                                {submission.testcase_results.length}
                                            </CardTitle>
                                        </CardHeader>
                                    </Card>
                                    <Card>
                                        <CardHeader className="p-4">
                                            <CardDescription className="text-xs">Time</CardDescription>
                                            <CardTitle className="text-2xl">{submission.execution_time}ms</CardTitle>
                                        </CardHeader>
                                    </Card>
                                    <Card>
                                        <CardHeader className="p-4">
                                            <CardDescription className="text-xs">Memory</CardDescription>
                                            <CardTitle className="text-2xl">
                                                {submission.memory_used ? `${submission.memory_used.toFixed(1)}MB` : "N/A"}
                                            </CardTitle>
                                        </CardHeader>
                                    </Card>
                                </div>

                                <Separator />

                                {/* Testcase Results */}
                                <div className="space-y-3">
                                    <h4 className="text-sm font-semibold">Testcase Results</h4>
                                    <ScrollArea className="h-[400px]">
                                        <div className="space-y-2 pr-4">
                                            {submission.testcase_results.map((result, idx) => (
                                                <Card
                                                    key={idx}
                                                    className={
                                                        result.status === "Passed"
                                                            ? "border-green-500/50"
                                                            : "border-red-500/50"
                                                    }
                                                >
                                                    <CardHeader className="p-4">
                                                        <div className="flex items-center justify-between">
                                                            <span className="text-sm font-medium">
                                                                {result.is_sample
                                                                    ? result.description || `Sample ${idx + 1}`
                                                                    : `Hidden Test ${idx + 1}`}
                                                            </span>
                                                            <Badge
                                                                variant={result.status === "Passed" ? "default" : "destructive"}
                                                            >
                                                                {result.status}
                                                            </Badge>
                                                        </div>
                                                        {result.is_sample && result.status !== "Passed" && (
                                                            <div className="mt-3 space-y-2 text-sm">
                                                                <div>
                                                                    <span className="text-muted-foreground">Expected:</span>
                                                                    <pre className="mt-1 bg-muted p-2 rounded text-xs overflow-x-auto">
                                                                        {result.expected_output}
                                                                    </pre>
                                                                </div>
                                                                <div>
                                                                    <span className="text-muted-foreground">Got:</span>
                                                                    <pre className="mt-1 bg-muted p-2 rounded text-xs overflow-x-auto">
                                                                        {result.actual_output || result.error_message}
                                                                    </pre>
                                                                </div>
                                                            </div>
                                                        )}
                                                    </CardHeader>
                                                </Card>
                                            ))}
                                        </div>
                                    </ScrollArea>
                                </div>
                            </CardContent>
                        </Card>

                        {/* AI Feedback */}
                        {aiFeedback ? (
                            <Card className="border-purple-500/50">
                                <CardHeader>
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="flex items-center gap-2">
                                            <Sparkles className="w-5 h-5 text-purple-500" />
                                            AI Feedback
                                        </CardTitle>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => loadAIFeedback(true)}
                                            disabled={loadingFeedback}
                                        >
                                            {loadingFeedback ? (
                                                <Loader2 className="w-4 h-4 animate-spin" />
                                            ) : (
                                                <RefreshCw className="w-4 h-4" />
                                            )}
                                        </Button>
                                    </div>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    {aiFeedback.overall_feedback && (
                                        <div>
                                            <h5 className="text-sm font-semibold mb-2">Overall Assessment</h5>
                                            <p className="text-sm text-muted-foreground leading-relaxed">
                                                {aiFeedback.overall_feedback}
                                            </p>
                                        </div>
                                    )}

                                    {aiFeedback.error_analysis && (
                                        <div>
                                            <h5 className="text-sm font-semibold mb-2 text-red-500">Error Analysis</h5>
                                            <p className="text-sm text-muted-foreground leading-relaxed">
                                                {aiFeedback.error_analysis}
                                            </p>
                                        </div>
                                    )}

                                    {aiFeedback.optimization_hints && (
                                        <div>
                                            <h5 className="text-sm font-semibold mb-2 text-blue-500">Optimization Hints</h5>
                                            <p className="text-sm text-muted-foreground leading-relaxed">
                                                {aiFeedback.optimization_hints}
                                            </p>
                                        </div>
                                    )}

                                    <div className="grid grid-cols-3 gap-3">
                                        <Card>
                                            <CardHeader className="p-3">
                                                <CardDescription className="text-xs">Time</CardDescription>
                                                <CardTitle className="text-sm">
                                                    {aiFeedback.time_complexity || "N/A"}
                                                </CardTitle>
                                            </CardHeader>
                                        </Card>
                                        <Card>
                                            <CardHeader className="p-3">
                                                <CardDescription className="text-xs">Space</CardDescription>
                                                <CardTitle className="text-sm">
                                                    {aiFeedback.space_complexity || "N/A"}
                                                </CardTitle>
                                            </CardHeader>
                                        </Card>
                                        <Card>
                                            <CardHeader className="p-3">
                                                <CardDescription className="text-xs">Quality</CardDescription>
                                                <CardTitle className="text-sm">
                                                    {aiFeedback.code_quality_score ? `${aiFeedback.code_quality_score}/100` : "N/A"}
                                                </CardTitle>
                                            </CardHeader>
                                        </Card>
                                    </div>
                                </CardContent>
                            </Card>
                        ) : (
                            <Button
                                onClick={() => loadAIFeedback(false)}
                                disabled={loadingFeedback}
                                className="w-full"
                                variant="outline"
                            >
                                {loadingFeedback ? (
                                    <>
                                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                        Generating AI Feedback...
                                    </>
                                ) : (
                                    <>
                                        <Sparkles className="w-4 h-4 mr-2" />
                                        Get AI Feedback
                                    </>
                                )}
                            </Button>
                        )}
                    </div>

                    {/* Right Column - Code */}
                    <div className="space-y-6">
                        <Card className="overflow-hidden">
                            <CardHeader className="bg-muted/50">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="flex gap-2">
                                            <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                                            <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                                            <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                                        </div>
                                        <span className="text-sm font-mono">
                                            submission.{submission.language === "cpp" ? "cpp" : "py"}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                        <Code className="w-4 h-4" />
                                        <span>{submission.language === "cpp" ? "C++" : "Python"}</span>
                                    </div>
                                </div>
                            </CardHeader>
                            <div style={{ height: "600px" }}>
                                <Editor
                                    height="100%"
                                    theme="vs-dark"
                                    language={submission.language === "cpp" ? "cpp" : "python"}
                                    value={submission.code}
                                    options={{
                                        readOnly: true,
                                        fontSize: 14,
                                        minimap: { enabled: false },
                                        padding: { top: 16, bottom: 16 },
                                        lineNumbers: "on",
                                        scrollBeyondLastLine: false,
                                        automaticLayout: true,
                                    }}
                                />
                            </div>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
