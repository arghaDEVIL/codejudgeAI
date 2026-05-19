import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardAPI, getUser, removeAuthToken } from '../utils/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { ThemeToggle } from '@/components/theme-toggle';
import {
    User,
    Trophy,
    Target,
    Clock,
    Code2,
    TrendingUp,
    Calendar,
    CheckCircle2,
    XCircle,
    AlertCircle,
    Users,
    History,
    LogOut,
    Award,
    Zap,
    Star,
    Activity,
    BarChart3,
    BookOpen,
    PieChart,
    LineChart
} from 'lucide-react';
import {
    AreaChart,
    Area,
    BarChart,
    Bar,
    PieChart as RechartsPieChart,
    Pie,
    Cell,
    LineChart as RechartsLineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

// Colors for charts
const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

export default function Dashboard() {
    const navigate = useNavigate();
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            setLoading(true);
            setError('');

            const response = await dashboardAPI.getStats();
            setDashboardData(response.data);

        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            setError('Failed to load dashboard data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'Accepted':
                return <CheckCircle2 className="h-4 w-4 text-green-500" />;
            case 'Wrong Answer':
            case 'Runtime Error':
                return <XCircle className="h-4 w-4 text-red-500" />;
            default:
                return <AlertCircle className="h-4 w-4 text-yellow-500" />;
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Accepted':
                return 'bg-green-500/10 text-green-500 border-green-500/20';
            case 'Wrong Answer':
            case 'Runtime Error':
                return 'bg-red-500/10 text-red-500 border-red-500/20';
            default:
                return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
        }
    };

    const getAchievementIcon = (iconName) => {
        const icons = {
            Trophy,
            Target,
            Award,
            Zap,
            Star,
            Activity,
            Code2
        };
        return icons[iconName] || Trophy;
    };

    const logout = () => {
        removeAuthToken();
        navigate('/login');
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <div className="text-center space-y-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
                    <p className="text-muted-foreground">Loading your dashboard...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <Card className="w-96">
                    <CardContent className="flex flex-col items-center gap-4 pt-6">
                        <AlertCircle className="h-16 w-16 text-destructive" />
                        <h2 className="text-xl font-semibold text-destructive">Error Loading Dashboard</h2>
                        <p className="text-muted-foreground text-center">{error}</p>
                        <Button onClick={loadDashboardData}>Try Again</Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    const { user, stats, recent_submissions, achievements, analytics } = dashboardData;

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                                <Code2 className="w-6 h-6 text-primary-foreground" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold">Dashboard</h1>
                                <p className="text-sm text-muted-foreground">Welcome back, {user?.name}!</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <ThemeToggle />
                        <Button variant="outline" onClick={() => navigate('/judge')}>
                            <BookOpen className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Problems</span>
                        </Button>
                        <Button variant="outline" onClick={() => navigate('/rooms')}>
                            <Users className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Rooms</span>
                        </Button>
                        <Button variant="outline" onClick={() => navigate('/history')}>
                            <History className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">History</span>
                        </Button>
                        <Button variant="destructive" onClick={logout}>
                            <LogOut className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Logout</span>
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <div className="container mx-auto px-6 py-8 space-y-8">
                {/* Stats Overview */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Problems Solved</CardTitle>
                            <Trophy className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-primary">{stats.solved_problems}</div>
                            <p className="text-xs text-muted-foreground">
                                {stats.total_submissions} total submissions
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
                            <Target className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-green-500">{stats.success_rate}%</div>
                            <p className="text-xs text-muted-foreground">
                                Accuracy in submissions
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
                            <Activity className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-orange-500">{stats.streak}</div>
                            <p className="text-xs text-muted-foreground">
                                Days of coding
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Rank</CardTitle>
                            <Award className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-purple-500">{stats.rank}</div>
                            <p className="text-xs text-muted-foreground">
                                Current skill level
                            </p>
                        </CardContent>
                    </Card>
                </div>

                {/* Analytics Charts */}
                {analytics && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Weekly Activity Chart */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <LineChart className="h-5 w-5" />
                                    Weekly Activity
                                </CardTitle>
                                <CardDescription>Your coding activity over the past 7 days</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ResponsiveContainer width="100%" height={300}>
                                    <AreaChart data={analytics.weekly_activity}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis
                                            dataKey="date"
                                            tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { weekday: 'short' })}
                                        />
                                        <YAxis />
                                        <Tooltip
                                            labelFormatter={(value) => new Date(value).toLocaleDateString()}
                                            formatter={(value) => [value, 'Submissions']}
                                        />
                                        <Area
                                            type="monotone"
                                            dataKey="submissions"
                                            stroke="hsl(var(--primary))"
                                            fill="hsl(var(--primary))"
                                            fillOpacity={0.3}
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>

                        {/* Language Distribution Chart */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <PieChart className="h-5 w-5" />
                                    Language Distribution
                                </CardTitle>
                                <CardDescription>Your preferred programming languages</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ResponsiveContainer width="100%" height={300}>
                                    <RechartsPieChart>
                                        <Pie
                                            data={analytics.language_distribution}
                                            cx="50%"
                                            cy="50%"
                                            labelLine={false}
                                            label={({ language, percent }) => `${language} ${(percent * 100).toFixed(0)}%`}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            dataKey="count"
                                        >
                                            {analytics.language_distribution.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip />
                                    </RechartsPieChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>

                        {/* Difficulty Progress Chart */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <BarChart3 className="h-5 w-5" />
                                    Problem Difficulty Progress
                                </CardTitle>
                                <CardDescription>Problems solved by difficulty level</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={analytics.difficulty_distribution}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="difficulty" />
                                        <YAxis />
                                        <Tooltip />
                                        <Bar dataKey="count" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>

                        {/* Success Rate Trend */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <TrendingUp className="h-5 w-5" />
                                    Success Rate Trend
                                </CardTitle>
                                <CardDescription>Your accuracy improvement over time</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ResponsiveContainer width="100%" height={300}>
                                    <RechartsLineChart data={analytics.weekly_activity}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis
                                            dataKey="date"
                                            tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                                        />
                                        <YAxis domain={[0, 100]} />
                                        <Tooltip
                                            labelFormatter={(value) => new Date(value).toLocaleDateString()}
                                            formatter={(value) => [`${value}%`, 'Success Rate']}
                                        />
                                        <Line
                                            type="monotone"
                                            dataKey="success_rate"
                                            stroke="hsl(var(--primary))"
                                            strokeWidth={2}
                                            dot={{ fill: 'hsl(var(--primary))' }}
                                        />
                                    </RechartsLineChart>
                                </ResponsiveContainer>
                            </CardContent>
                        </Card>
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Recent Activity */}
                    <div className="lg:col-span-2 space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Clock className="h-5 w-5" />
                                    Recent Submissions
                                </CardTitle>
                                <CardDescription>Your latest coding activity</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ScrollArea className="h-[400px]">
                                    <div className="space-y-4">
                                        {recent_submissions && recent_submissions.length > 0 ? (
                                            recent_submissions.map((submission) => (
                                                <div
                                                    key={submission.id}
                                                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors cursor-pointer"
                                                    onClick={() => navigate(`/submission/${submission.id}`)}
                                                >
                                                    <div className="flex items-center gap-3">
                                                        {getStatusIcon(submission.status)}
                                                        <div>
                                                            <p className="font-medium">Problem #{submission.problem_id}</p>
                                                            <p className="text-sm text-muted-foreground">
                                                                {submission.language} • {new Date(submission.created_at).toLocaleDateString()}
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <Badge variant="outline" className={getStatusColor(submission.status)}>
                                                        {submission.status}
                                                    </Badge>
                                                </div>
                                            ))
                                        ) : (
                                            <div className="text-center py-8 text-muted-foreground">
                                                <Code2 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                                <p>No submissions yet</p>
                                                <p className="text-sm">Start solving problems to see your activity here!</p>
                                            </div>
                                        )}
                                    </div>
                                </ScrollArea>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Profile Info */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <User className="h-5 w-5" />
                                    Profile
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center">
                                        <span className="text-lg font-bold text-primary-foreground">
                                            {user?.name?.charAt(0).toUpperCase()}
                                        </span>
                                    </div>
                                    <div>
                                        <p className="font-semibold">{user?.name}</p>
                                        <p className="text-sm text-muted-foreground">{user?.email}</p>
                                    </div>
                                </div>
                                <Separator />
                                <div className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="text-sm text-muted-foreground">Favorite Language</span>
                                        <Badge variant="secondary">{stats.favorite_language}</Badge>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sm text-muted-foreground">Time Spent</span>
                                        <span className="text-sm font-medium">{Math.round(stats.total_time_minutes / 60)}h</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sm text-muted-foreground">Member Since</span>
                                        <span className="text-sm font-medium">
                                            {new Date(user?.created_at || Date.now()).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Achievements */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Award className="h-5 w-5" />
                                    Achievements
                                </CardTitle>
                                <CardDescription>Your coding milestones</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ScrollArea className="h-[300px]">
                                    <div className="space-y-3">
                                        {achievements && achievements.map((achievement) => {
                                            const IconComponent = getAchievementIcon(achievement.icon);
                                            return (
                                                <div
                                                    key={achievement.id}
                                                    className={`flex items-center gap-3 p-3 rounded-lg border ${achievement.earned
                                                        ? 'bg-accent/50 border-primary/20'
                                                        : 'bg-muted/30 border-muted'
                                                        }`}
                                                >
                                                    <IconComponent className={`h-6 w-6 ${achievement.color}`} />
                                                    <div className="flex-1">
                                                        <p className={`font-medium ${!achievement.earned && 'text-muted-foreground'}`}>
                                                            {achievement.title}
                                                        </p>
                                                        <p className="text-xs text-muted-foreground">
                                                            {achievement.description}
                                                        </p>
                                                        {!achievement.earned && achievement.progress !== undefined && (
                                                            <div className="mt-1">
                                                                <div className="flex justify-between text-xs text-muted-foreground">
                                                                    <span>{achievement.progress}/{achievement.target}</span>
                                                                    <span>{Math.round((achievement.progress / achievement.target) * 100)}%</span>
                                                                </div>
                                                                <div className="w-full bg-muted rounded-full h-1 mt-1">
                                                                    <div
                                                                        className="bg-primary h-1 rounded-full transition-all"
                                                                        style={{ width: `${(achievement.progress / achievement.target) * 100}%` }}
                                                                    />
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </ScrollArea>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}