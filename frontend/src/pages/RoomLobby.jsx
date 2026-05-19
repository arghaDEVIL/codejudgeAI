import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { roomsAPI, problemsAPI } from '../utils/api';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { ThemeToggle } from "@/components/theme-toggle";
import {
    ArrowLeft,
    Plus,
    Link2,
    Users,
    Sparkles,
    Loader2,
    RefreshCw,
    ChevronRight,
    Briefcase,
    BookOpen,
    UsersRound,
    AlertCircle,
    User,
    Code
} from 'lucide-react';

const RoomLobby = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [userRooms, setUserRooms] = useState([]);
    const [loadingRooms, setLoadingRooms] = useState(true);
    const [problems, setProblems] = useState([]);

    const [createForm, setCreateForm] = useState({
        title: '',
        description: '',
        mode: 'collaborative',
        max_participants: 10,
        problem_id: null,
    });

    const [joinCode, setJoinCode] = useState('');

    useEffect(() => {
        loadUserRooms();
        loadProblems();
    }, []);

    const loadProblems = async () => {
        try {
            const response = await problemsAPI.getAll();
            setProblems(response.data);
        } catch (err) {
            console.error('Failed to load problems:', err);
        }
    };

    const loadUserRooms = async () => {
        setLoadingRooms(true);
        try {
            const response = await roomsAPI.getUserRooms();
            setUserRooms(response.data);
        } catch (err) {
            console.error('Failed to load rooms:', err);
        } finally {
            setLoadingRooms(false);
        }
    };

    const handleCreateRoom = async (e) => {
        e.preventDefault();
        if (!createForm.title.trim()) {
            setError('Please enter a room title');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await roomsAPI.create(createForm);
            navigate(`/room/${response.data.room_code}`);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create room');
        } finally {
            setLoading(false);
        }
    };

    const handleJoinRoom = async (e) => {
        e.preventDefault();
        if (!joinCode.trim()) {
            setError('Please enter a room code');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            const displayName = user.name || user.email || 'Anonymous';
            await roomsAPI.join(joinCode.toUpperCase(), { display_name: displayName });
            navigate(`/room/${joinCode.toUpperCase()}`);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to join room');
        } finally {
            setLoading(false);
        }
    };

    const handleRoomClick = async (roomCode) => {
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            const displayName = user.name || user.email || 'Anonymous';
            await roomsAPI.join(roomCode, { display_name: displayName });
        } catch (err) {
            console.log('Join room error (continuing anyway):', err);
        }
        navigate(`/room/${roomCode}`);
    };

    const getModeIcon = (mode) => {
        if (mode === 'interview') return <Briefcase className="w-4 h-4" />;
        if (mode === 'practice') return <BookOpen className="w-4 h-4" />;
        return <UsersRound className="w-4 h-4" />;
    };

    const getModeVariant = (mode) => {
        if (mode === 'interview') return 'destructive';
        if (mode === 'practice') return 'secondary';
        return 'default';
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b sticky top-0 z-50 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate('/judge')}>
                            <ArrowLeft className="w-5 h-5" />
                        </Button>
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                                <Code className="w-6 h-6 text-primary-foreground" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold">Collaborative Rooms</h1>
                                <p className="text-sm text-muted-foreground">Code together in real-time</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <ThemeToggle />
                        <Button variant="outline" size="sm" onClick={() => navigate('/dashboard')}>
                            <User className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Dashboard</span>
                        </Button>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto p-6 space-y-6">
                {/* Error Alert */}
                {error && (
                    <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                {/* Create & Join Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Create Room */}
                    <Card>
                        <CardHeader>
                            <div className="flex items-center gap-2">
                                <Sparkles className="w-5 h-5 text-primary" />
                                <CardTitle>Create New Room</CardTitle>
                            </div>
                            <CardDescription>Start a new collaborative session</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleCreateRoom} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="title">Room Title</Label>
                                    <Input
                                        id="title"
                                        value={createForm.title}
                                        onChange={(e) => setCreateForm({ ...createForm, title: e.target.value })}
                                        placeholder="e.g., Algorithm Study Session"
                                        required
                                        maxLength={200}
                                    />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="description">Description (Optional)</Label>
                                    <Textarea
                                        id="description"
                                        value={createForm.description}
                                        onChange={(e) => setCreateForm({ ...createForm, description: e.target.value })}
                                        placeholder="What will you be working on?"
                                        rows={3}
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="mode">Mode</Label>
                                        <Select
                                            value={createForm.mode}
                                            onValueChange={(value) => setCreateForm({ ...createForm, mode: value })}
                                        >
                                            <SelectTrigger id="mode">
                                                <SelectValue />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="collaborative">👥 Collaborative</SelectItem>
                                                <SelectItem value="interview">💼 Interview</SelectItem>
                                                <SelectItem value="practice">📚 Practice</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="max_participants">Max Users</Label>
                                        <Input
                                            id="max_participants"
                                            type="number"
                                            value={createForm.max_participants}
                                            onChange={(e) => setCreateForm({ ...createForm, max_participants: parseInt(e.target.value) })}
                                            min={2}
                                            max={50}
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="problem">Problem (Optional)</Label>
                                    <Select
                                        value={createForm.problem_id?.toString() || 'none'}
                                        onValueChange={(value) => setCreateForm({ ...createForm, problem_id: value === 'none' ? null : parseInt(value) })}
                                    >
                                        <SelectTrigger id="problem">
                                            <SelectValue placeholder="No problem - Free coding" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="none">No problem - Free coding</SelectItem>
                                            {problems.map((problem) => (
                                                <SelectItem key={problem.id} value={problem.id.toString()}>
                                                    {problem.title} ({problem.difficulty})
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    <p className="text-xs text-muted-foreground">Select a problem to solve together</p>
                                </div>

                                <Button type="submit" className="w-full" disabled={loading}>
                                    {loading ? (
                                        <>
                                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                            Creating...
                                        </>
                                    ) : (
                                        <>
                                            <Plus className="w-4 h-4 mr-2" />
                                            Create Room
                                        </>
                                    )}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    {/* Join Room */}
                    <Card>
                        <CardHeader>
                            <div className="flex items-center gap-2">
                                <Link2 className="w-5 h-5 text-primary" />
                                <CardTitle>Join Existing Room</CardTitle>
                            </div>
                            <CardDescription>Enter a room code to join</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <form onSubmit={handleJoinRoom} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="joinCode">Room Code</Label>
                                    <Input
                                        id="joinCode"
                                        value={joinCode}
                                        onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                                        placeholder="ABC12XYZ"
                                        maxLength={8}
                                        className="font-mono text-lg tracking-wider"
                                    />
                                    <p className="text-xs text-muted-foreground">8-character code from your teammate</p>
                                </div>

                                <Button type="submit" className="w-full" variant="secondary" disabled={loading}>
                                    {loading ? (
                                        <>
                                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                            Joining...
                                        </>
                                    ) : (
                                        <>
                                            <Link2 className="w-4 h-4 mr-2" />
                                            Join Room
                                        </>
                                    )}
                                </Button>
                            </form>

                            <Separator />

                            <div className="space-y-2">
                                <h4 className="text-sm font-semibold">💡 Quick Guide</h4>
                                <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                                    <li>Get the room code from your host</li>
                                    <li>Enter it in the field above</li>
                                    <li>Click join and start coding!</li>
                                </ul>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* User's Rooms */}
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Users className="w-5 h-5 text-primary" />
                                <CardTitle>Your Active Rooms</CardTitle>
                            </div>
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={loadUserRooms}
                                disabled={loadingRooms}
                            >
                                <RefreshCw className={`w-4 h-4 ${loadingRooms ? 'animate-spin' : ''}`} />
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        {loadingRooms ? (
                            <div className="flex flex-col items-center justify-center py-12">
                                <Loader2 className="w-12 h-12 animate-spin text-primary mb-4" />
                                <p className="text-muted-foreground">Loading your rooms...</p>
                            </div>
                        ) : userRooms.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {userRooms.map((room) => (
                                    <Card
                                        key={room.id}
                                        className="cursor-pointer hover:shadow-md transition-all"
                                        onClick={() => handleRoomClick(room.room_code)}
                                    >
                                        <CardHeader className="pb-3">
                                            <div className="flex items-start justify-between gap-2">
                                                <div className="flex items-center gap-2 flex-1">
                                                    {getModeIcon(room.mode)}
                                                    <CardTitle className="text-base line-clamp-1">{room.title}</CardTitle>
                                                </div>
                                                <Badge variant="outline" className="font-mono text-xs">
                                                    {room.room_code}
                                                </Badge>
                                            </div>
                                            {room.description && (
                                                <CardDescription className="line-clamp-2">
                                                    {room.description}
                                                </CardDescription>
                                            )}
                                        </CardHeader>
                                        <CardContent className="pt-0">
                                            <div className="flex items-center justify-between">
                                                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                                    <Users className="w-4 h-4" />
                                                    <span>{room.participant_count}/{room.max_participants}</span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <Badge variant={getModeVariant(room.mode)} className="text-xs">
                                                        {room.mode}
                                                    </Badge>
                                                    <Badge variant={room.status === 'active' ? 'default' : 'secondary'} className="text-xs">
                                                        {room.status}
                                                    </Badge>
                                                </div>
                                                <ChevronRight className="w-4 h-4 text-muted-foreground" />
                                            </div>
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>
                        ) : (
                            <div className="flex flex-col items-center justify-center py-12 text-center">
                                <Users className="w-16 h-16 text-muted-foreground mb-4" />
                                <h3 className="text-lg font-semibold mb-2">No rooms yet</h3>
                                <p className="text-muted-foreground">
                                    Create a new room or join an existing one to get started
                                </p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default RoomLobby;
