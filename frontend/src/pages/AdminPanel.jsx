import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUser, removeAuthToken } from '../utils/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { ThemeToggle } from '@/components/theme-toggle';
import {
    Settings,
    Download,
    BarChart3,
    Users,
    FileText,
    Activity,
    LogOut,
    User,
    AlertCircle,
    CheckCircle2,
    Clock,
    Database
} from 'lucide-react';
import api from '../utils/api';

export default function AdminPanel() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [importStatus, setImportStatus] = useState('');
    const [stats, setStats] = useState(null);
    const [systemInfo, setSystemInfo] = useState(null);

    // Import settings
    const [importSource, setImportSource] = useState('sample');
    const [importLimit, setImportLimit] = useState(20);
    const [minRating, setMinRating] = useState(800);
    const [maxRating, setMaxRating] = useState(1600);

    const user = getUser();

    useEffect(() => {
        // Check if user is admin
        if (!user?.is_admin) {
            navigate('/dashboard');
            return;
        }

        loadStats();
        loadSystemInfo();
    }, [user, navigate]);

    const loadStats = async () => {
        try {
            const response = await api.get('/admin/problem-stats');
            setStats(response.data.stats);
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    };

    const loadSystemInfo = async () => {
        try {
            const response = await api.get('/admin/system-info');
            setSystemInfo(response.data);
        } catch (error) {
            console.error('Failed to load system info:', error);
        }
    };

    const handleImport = async () => {
        try {
            setLoading(true);
            setImportStatus('Starting import...');

            const response = await api.post('/admin/import-problems', null, {
                params: {
                    source: importSource,
                    limit: importLimit,
                    min_rating: minRating,
                    max_rating: maxRating
                }
            });

            setImportStatus('Import started successfully! Check back in a few moments.');

            // Refresh stats after a delay
            setTimeout(() => {
                loadStats();
                loadSystemInfo();
                setImportStatus('');
            }, 3000);

        } catch (error) {
            console.error('Import failed:', error);
            setImportStatus('Import failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        removeAuthToken();
        navigate('/login');
    };

    if (!user?.is_admin) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <Card className="w-96">
                    <CardContent className="flex flex-col items-center gap-4 pt-6">
                        <AlertCircle className="h-16 w-16 text-destructive" />
                        <h2 className="text-xl font-semibold text-destructive">Access Denied</h2>
                        <p className="text-muted-foreground text-center">
                            You need admin privileges to access this page.
                        </p>
                        <Button onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                                <Settings className="w-6 h-6 text-primary-foreground" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold">Admin Panel</h1>
                                <p className="text-sm text-muted-foreground">System Management</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <ThemeToggle />
                        <Button variant="outline" onClick={() => navigate('/dashboard')}>
                            <User className="w-4 h-4 mr-2" />
                            Dashboard
                        </Button>
                        <Button variant="destructive" onClick={logout}>
                            <LogOut className="w-4 h-4 mr-2" />
                            Logout
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <div className="container mx-auto px-6 py-8 space-y-8">
                {/* System Overview */}
                {systemInfo && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Total Problems</CardTitle>
                                <FileText className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-primary">
                                    {systemInfo.system_stats.total_problems}
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                                <Users className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-blue-500">
                                    {systemInfo.system_stats.total_users}
                                </div>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Total Submissions</CardTitle>
                                <Activity className="h-4 w-4 text-muted-foreground" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-green-500">
                                    {systemInfo.system_stats.total_submissions}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Problem Import */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Download className="h-5 w-5" />
                                Import Problems
                            </CardTitle>
                            <CardDescription>
                                Automatically import problems from various coding platforms
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Import Source</label>
                                <Select value={importSource} onValueChange={setImportSource}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="sample">📚 Sample Problems (6 curated)</SelectItem>
                                        <SelectItem value="codeforces">🏆 Codeforces API</SelectItem>
                                        <SelectItem value="all">🚀 Sample + Codeforces</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            {importSource !== 'sample' && (
                                <>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Limit</label>
                                            <Input
                                                type="number"
                                                value={importLimit}
                                                onChange={(e) => setImportLimit(parseInt(e.target.value) || 20)}
                                                min="1"
                                                max="100"
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Min Rating</label>
                                            <Input
                                                type="number"
                                                value={minRating}
                                                onChange={(e) => setMinRating(parseInt(e.target.value) || 800)}
                                                min="800"
                                                max="3000"
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Max Rating</label>
                                        <Input
                                            type="number"
                                            value={maxRating}
                                            onChange={(e) => setMaxRating(parseInt(e.target.value) || 1600)}
                                            min="800"
                                            max="3000"
                                        />
                                    </div>
                                </>
                            )}

                            <Button
                                onClick={handleImport}
                                disabled={loading}
                                className="w-full"
                                size="lg"
                            >
                                {loading ? (
                                    <>
                                        <Clock className="w-4 h-4 mr-2 animate-spin" />
                                        Importing...
                                    </>
                                ) : (
                                    <>
                                        <Download className="w-4 h-4 mr-2" />
                                        Start Import
                                    </>
                                )}
                            </Button>

                            {importStatus && (
                                <div className="flex items-center gap-2 p-3 bg-muted rounded-lg">
                                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                                    <span className="text-sm">{importStatus}</span>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Problem Statistics */}
                    {stats && (
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <BarChart3 className="h-5 w-5" />
                                    Problem Statistics
                                </CardTitle>
                                <CardDescription>Current problem database overview</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid grid-cols-3 gap-4">
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-green-500">
                                            {stats.difficulty_distribution?.Easy || 0}
                                        </div>
                                        <div className="text-sm text-muted-foreground">Easy</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-yellow-500">
                                            {stats.difficulty_distribution?.Medium || 0}
                                        </div>
                                        <div className="text-sm text-muted-foreground">Medium</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-red-500">
                                            {stats.difficulty_distribution?.Hard || 0}
                                        </div>
                                        <div className="text-sm text-muted-foreground">Hard</div>
                                    </div>
                                </div>

                                <Separator />

                                <div>
                                    <h4 className="font-medium mb-2">Top Tags</h4>
                                    <div className="flex flex-wrap gap-1">
                                        {stats.top_tags?.slice(0, 8).map(([tag, count]) => (
                                            <Badge key={tag} variant="secondary" className="text-xs">
                                                {tag} ({count})
                                            </Badge>
                                        ))}
                                    </div>
                                </div>

                                <div className="text-center pt-2">
                                    <div className="text-lg font-semibold">
                                        {stats.total_problems} Total Problems
                                    </div>
                                    <div className="text-sm text-muted-foreground">
                                        {stats.total_tags} Unique Tags
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Recent Activity */}
                {systemInfo?.recent_activity && (
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Activity className="h-5 w-5" />
                                Recent Submissions
                            </CardTitle>
                            <CardDescription>Latest user activity</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {systemInfo.recent_activity.map((submission) => (
                                    <div key={submission.id} className="flex items-center justify-between p-3 border rounded-lg">
                                        <div className="flex items-center gap-3">
                                            <Database className="w-4 h-4 text-muted-foreground" />
                                            <div>
                                                <p className="font-medium">
                                                    User #{submission.user_id} • Problem #{submission.problem_id}
                                                </p>
                                                <p className="text-sm text-muted-foreground">
                                                    {new Date(submission.created_at).toLocaleString()}
                                                </p>
                                            </div>
                                        </div>
                                        <Badge
                                            variant={submission.status === 'Accepted' ? 'default' : 'destructive'}
                                        >
                                            {submission.status}
                                        </Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}