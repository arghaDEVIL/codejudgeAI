import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { submissionsAPI, problemsAPI, removeAuthToken } from "./utils/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Pagination } from "@/components/ui/pagination";
import {
    ArrowLeft,
    LogOut,
    Code,
    CheckCircle2,
    XCircle,
    Clock,
    Cpu,
    Calendar,
    ChevronRight,
    Loader2,
    FileText
} from "lucide-react";

export default function SubmissionHistory() {
    const [submissions, setSubmissions] = useState([]);
    const [problems, setProblems] = useState({});
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState("all");
    const navigate = useNavigate();

    // Pagination states
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalSubmissions, setTotalSubmissions] = useState(0);
    const [submissionsPerPage] = useState(20);

    useEffect(() => {
        loadData();
    }, [currentPage, filter]);

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const loadData = async () => {
        try {
            setLoading(true);

            // Load submissions with pagination
            const params = {
                page: currentPage,
                limit: submissionsPerPage
            };

            const subRes = await submissionsAPI.getUserSubmissions(params);
            setSubmissions(subRes.data);

            // Extract pagination info from headers
            const totalCount = parseInt(subRes.headers['x-total-count'] || '0');
            const totalPagesCount = parseInt(subRes.headers['x-total-pages'] || '1');

            setTotalSubmissions(totalCount);
            setTotalPages(totalPagesCount);

            // Load problems (cache this to avoid repeated calls)
            if (Object.keys(problems).length === 0) {
                const probRes = await problemsAPI.getAll();
                const probMap = {};
                probRes.data.forEach(p => {
                    probMap[p.id] = p;
                });
                setProblems(probMap);
            }
        } catch (error) {
            console.error("Failed to load submissions:", error);
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        removeAuthToken();
        window.location.href = "/login";
    };

    const getStatusVariant = (status) => {
        if (status === "Accepted") return "default";
        if (status === "Wrong Answer") return "destructive";
        if (status === "Runtime Error") return "secondary";
        return "outline";
    };

    const getStatusIcon = (status) => {
        if (status === "Accepted") return <CheckCircle2 className="w-4 h-4" />;
        if (status === "Wrong Answer") return <XCircle className="w-4 h-4" />;
        return <Clock className="w-4 h-4" />;
    };

    const filteredSubmissions = filter === "all"
        ? submissions
        : filter === "accepted"
            ? submissions.filter(sub => sub.status === "Accepted")
            : submissions.filter(sub => sub.status !== "Accepted");

    const getFilteredCount = (filterType) => {
        if (filterType === "all") return totalSubmissions;
        if (filterType === "accepted") {
            return submissions.filter(s => s.status === "Accepted").length;
        }
        return submissions.filter(s => s.status !== "Accepted").length;
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b sticky top-0 z-50 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate("/judge")}>
                            <ArrowLeft className="w-5 h-5" />
                        </Button>
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                                <FileText className="w-6 h-6 text-primary-foreground" />
                            </div>
                            <h1 className="text-2xl font-bold">Submission History</h1>
                        </div>
                    </div>

                    <Button variant="destructive" onClick={logout}>
                        <LogOut className="w-4 h-4 mr-2" />
                        <span className="hidden sm:inline">Logout</span>
                    </Button>
                </div>
            </header>

            <div className="max-w-7xl mx-auto p-6">
                {/* Filters */}
                <div className="flex items-center gap-3 mb-6">
                    <Button
                        variant={filter === "all" ? "default" : "outline"}
                        onClick={() => { setFilter("all"); setCurrentPage(1); }}
                    >
                        All ({totalSubmissions})
                    </Button>
                    <Button
                        variant={filter === "accepted" ? "default" : "outline"}
                        onClick={() => { setFilter("accepted"); setCurrentPage(1); }}
                    >
                        Accepted ({getFilteredCount("accepted")})
                    </Button>
                    <Button
                        variant={filter === "failed" ? "default" : "outline"}
                        onClick={() => { setFilter("failed"); setCurrentPage(1); }}
                    >
                        Failed ({getFilteredCount("failed")})
                    </Button>
                </div>

                {/* Submissions List */}
                {loading ? (
                    <div className="flex items-center justify-center py-20">
                        <Loader2 className="w-12 h-12 animate-spin text-primary" />
                    </div>
                ) : filteredSubmissions.length === 0 ? (
                    <Card className="text-center py-20">
                        <CardContent className="space-y-4">
                            <FileText className="w-24 h-24 mx-auto text-muted-foreground" />
                            <CardTitle className="text-2xl">No Submissions Yet</CardTitle>
                            <CardDescription>
                                Start solving problems to see your submission history
                            </CardDescription>
                            <Button onClick={() => navigate("/judge")} className="mt-4">
                                Go to Problems
                            </Button>
                        </CardContent>
                    </Card>
                ) : (
                    <div className="space-y-4">
                        {filteredSubmissions.map((submission) => (
                            <Card
                                key={submission.id}
                                className="cursor-pointer hover:shadow-md transition-all"
                                onClick={() => navigate(`/submission/${submission.id}`)}
                            >
                                <CardHeader>
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="flex-1 space-y-2">
                                            <div className="flex items-center gap-3">
                                                <CardTitle className="text-xl">
                                                    {problems[submission.problem_id]?.title || `Problem #${submission.problem_id}`}
                                                </CardTitle>
                                                <Badge variant={getStatusVariant(submission.status)} className="flex items-center gap-1">
                                                    {getStatusIcon(submission.status)}
                                                    {submission.status}
                                                </Badge>
                                            </div>

                                            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                                                <div className="flex items-center gap-2">
                                                    <Code className="w-4 h-4" />
                                                    <span>{submission.language === "python" ? "Python" : "C++"}</span>
                                                </div>

                                                <div className="flex items-center gap-2">
                                                    <Badge variant="secondary" className="font-semibold">
                                                        {submission.score?.toFixed(1) || 0}/100
                                                    </Badge>
                                                </div>

                                                <div className="flex items-center gap-2">
                                                    <CheckCircle2 className="w-4 h-4" />
                                                    <span>{submission.passed_testcases}/{submission.total_testcases} tests</span>
                                                </div>

                                                {submission.execution_time && (
                                                    <div className="flex items-center gap-2">
                                                        <Clock className="w-4 h-4" />
                                                        <span>{submission.execution_time}ms</span>
                                                    </div>
                                                )}

                                                {submission.memory_used && (
                                                    <div className="flex items-center gap-2">
                                                        <Cpu className="w-4 h-4" />
                                                        <span>{submission.memory_used.toFixed(2)} MB</span>
                                                    </div>
                                                )}

                                                <div className="flex items-center gap-2">
                                                    <Calendar className="w-4 h-4" />
                                                    <span>{formatDate(submission.created_at)}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <ChevronRight className="w-6 h-6 text-muted-foreground flex-shrink-0" />
                                    </div>
                                </CardHeader>
                            </Card>
                        ))}

                        {/* Pagination */}
                        {totalPages > 1 && (
                            <div className="mt-6">
                                <Pagination
                                    currentPage={currentPage}
                                    totalPages={totalPages}
                                    onPageChange={handlePageChange}
                                    totalItems={totalSubmissions}
                                    itemsPerPage={submissionsPerPage}
                                />
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
