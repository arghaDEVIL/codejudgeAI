import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { problemsAPI, submissionsAPI, testcasesAPI, getUser, removeAuthToken } from "./utils/api";
import Editor from "@monaco-editor/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import {
    Code, Play, History, Users, LogOut, Menu, CheckCircle2, XCircle, AlertCircle, Clock, User,
    Search, Filter, X, Tag
} from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";
import { Pagination } from "@/components/ui/pagination";

export default function Judge() {
    const navigate = useNavigate();
    const [problems, setProblems] = useState([]);
    const [filteredProblems, setFilteredProblems] = useState([]);
    const [selected, setSelected] = useState(null);
    const [code, setCode] = useState("print('hello')");
    const [language, setLanguage] = useState("python");
    const [loading, setLoading] = useState(false);
    const [showSidebar, setShowSidebar] = useState(true);
    const [testcases, setTestcases] = useState([]);
    const [submissionResult, setSubmissionResult] = useState(null);

    // Filtering states
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedDifficulty, setSelectedDifficulty] = useState("all");
    const [selectedTags, setSelectedTags] = useState([]);
    const [availableTags, setAvailableTags] = useState([]);
    const [problemStats, setProblemStats] = useState(null);
    const [showFilters, setShowFilters] = useState(false);

    // Pagination states
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalProblems, setTotalProblems] = useState(0);
    const [problemsPerPage] = useState(10);

    const user = getUser();

    useEffect(() => {
        loadProblems();
        loadTags();
        loadStats();
    }, []);

    useEffect(() => {
        if (selected) {
            loadTestcases();
            setSubmissionResult(null);
        }
    }, [selected]);

    useEffect(() => {
        loadProblems();
    }, [currentPage, searchTerm, selectedDifficulty, selectedTags]);

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const loadProblems = async () => {
        try {
            const params = {
                page: currentPage,
                limit: problemsPerPage
            };

            if (selectedDifficulty !== "all") {
                params.difficulty = selectedDifficulty;
            }

            if (selectedTags.length > 0) {
                params.tags = selectedTags.join(",");
            }

            if (searchTerm) {
                params.search = searchTerm;
            }

            const res = await problemsAPI.getAll(params);
            setProblems(res.data);
            setFilteredProblems(res.data);

            // Extract pagination info from headers
            const totalCount = parseInt(res.headers['x-total-count'] || '0');
            const totalPagesCount = parseInt(res.headers['x-total-pages'] || '1');

            setTotalProblems(totalCount);
            setTotalPages(totalPagesCount);

            if (res.data.length > 0 && !selected) {
                setSelected(res.data[0]);
            }
        } catch (error) {
            console.error("Failed to load problems:", error);
        }
    };

    const loadTags = async () => {
        try {
            const res = await problemsAPI.getTags();
            setAvailableTags(res.data);
        } catch (error) {
            console.error("Failed to load tags:", error);
        }
    };

    const loadStats = async () => {
        try {
            const res = await problemsAPI.getStats();
            setProblemStats(res.data);
        } catch (error) {
            console.error("Failed to load stats:", error);
        }
    };

    const toggleTag = (tag) => {
        setSelectedTags(prev =>
            prev.includes(tag)
                ? prev.filter(t => t !== tag)
                : [...prev, tag]
        );
    };

    const clearFilters = () => {
        setSearchTerm("");
        setSelectedDifficulty("all");
        setSelectedTags([]);
    };

    const loadTestcases = async () => {
        try {
            const res = await testcasesAPI.getByProblem(selected.id);
            setTestcases(res.data);
        } catch (error) {
            console.error("Failed to load testcases:", error);
            setTestcases([]);
        }
    };

    const submitCode = async () => {
        if (!selected) return;

        try {
            setLoading(true);
            setSubmissionResult(null);

            const res = await submissionsAPI.submit({
                problem_id: selected.id,
                code,
                language,
            });

            setSubmissionResult(res.data);
        } catch (error) {
            console.error("Submission error:", error);
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        removeAuthToken();
        window.location.href = "/login";
    };

    const getDifficultyVariant = (difficulty) => {
        const variants = {
            Easy: "default",
            Medium: "secondary",
            Hard: "destructive",
        };
        return variants[difficulty] || "outline";
    };

    const getStatusIcon = (status) => {
        if (status === "Accepted") return <CheckCircle2 className="w-5 h-5" />;
        if (status === "Wrong Answer") return <XCircle className="w-5 h-5" />;
        if (status === "Runtime Error") return <AlertCircle className="w-5 h-5" />;
        if (status === "Time Limit Exceeded") return <Clock className="w-5 h-5" />;
        return <AlertCircle className="w-5 h-5" />;
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b sticky top-0 z-50 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
                <div className="flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-4">
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setShowSidebar(!showSidebar)}
                            className="lg:hidden"
                        >
                            <Menu className="w-5 h-5" />
                        </Button>
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                                <Code className="w-6 h-6 text-primary-foreground" />
                            </div>
                            <h1 className="text-2xl font-bold">CodeJudge</h1>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <ThemeToggle />
                        <Button variant="outline" onClick={() => navigate("/dashboard")}>
                            <User className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Dashboard</span>
                        </Button>
                        <Button variant="outline" onClick={() => navigate("/rooms")}>
                            <Users className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Rooms</span>
                        </Button>
                        <Button variant="outline" onClick={() => navigate("/history")}>
                            <History className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">History</span>
                        </Button>
                        <Button variant="ghost" className="hidden sm:flex">
                            {user?.name || `User #${user?.id}`}
                        </Button>
                        <Button variant="destructive" onClick={logout}>
                            <LogOut className="w-4 h-4 mr-2" />
                            <span className="hidden sm:inline">Logout</span>
                        </Button>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-12 h-[calc(100vh-73px)]">
                {/* Sidebar - Problems List */}
                {showSidebar && (
                    <div className="col-span-12 lg:col-span-3 border-r">
                        <ScrollArea className="h-full">
                            <div className="p-4 space-y-4">
                                {/* Header with Stats */}
                                <div className="flex items-center justify-between">
                                    <h2 className="text-lg font-semibold">Problems</h2>
                                    <div className="flex items-center gap-2">
                                        <Badge variant="secondary">{filteredProblems.length}</Badge>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => setShowFilters(!showFilters)}
                                        >
                                            <Filter className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </div>

                                {/* Quick Stats */}
                                {problemStats && (
                                    <div className="grid grid-cols-3 gap-2">
                                        <Card className="p-2">
                                            <div className="text-center">
                                                <div className="text-lg font-bold text-green-500">
                                                    {problemStats.difficulty_counts.Easy}
                                                </div>
                                                <div className="text-xs text-muted-foreground">Easy</div>
                                            </div>
                                        </Card>
                                        <Card className="p-2">
                                            <div className="text-center">
                                                <div className="text-lg font-bold text-yellow-500">
                                                    {problemStats.difficulty_counts.Medium}
                                                </div>
                                                <div className="text-xs text-muted-foreground">Medium</div>
                                            </div>
                                        </Card>
                                        <Card className="p-2">
                                            <div className="text-center">
                                                <div className="text-lg font-bold text-red-500">
                                                    {problemStats.difficulty_counts.Hard}
                                                </div>
                                                <div className="text-xs text-muted-foreground">Hard</div>
                                            </div>
                                        </Card>
                                    </div>
                                )}

                                {/* Filters */}
                                {showFilters && (
                                    <Card className="p-4 space-y-4">
                                        <div className="flex items-center justify-between">
                                            <h3 className="font-medium">Filters</h3>
                                            <Button variant="ghost" size="sm" onClick={clearFilters}>
                                                Clear All
                                            </Button>
                                        </div>

                                        {/* Search */}
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Search</label>
                                            <div className="relative">
                                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                                <Input
                                                    placeholder="Search problems..."
                                                    value={searchTerm}
                                                    onChange={(e) => setSearchTerm(e.target.value)}
                                                    className="pl-10"
                                                />
                                            </div>
                                        </div>

                                        {/* Difficulty Filter */}
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Difficulty</label>
                                            <Select value={selectedDifficulty} onValueChange={setSelectedDifficulty}>
                                                <SelectTrigger>
                                                    <SelectValue />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="all">All Difficulties</SelectItem>
                                                    <SelectItem value="Easy">🟢 Easy</SelectItem>
                                                    <SelectItem value="Medium">🟡 Medium</SelectItem>
                                                    <SelectItem value="Hard">🔴 Hard</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>

                                        {/* Tags Filter */}
                                        <div className="space-y-2">
                                            <label className="text-sm font-medium">Topics</label>
                                            <div className="flex flex-wrap gap-1 max-h-32 overflow-y-auto">
                                                {availableTags.map((tag) => (
                                                    <Badge
                                                        key={tag}
                                                        variant={selectedTags.includes(tag) ? "default" : "outline"}
                                                        className="cursor-pointer text-xs"
                                                        onClick={() => toggleTag(tag)}
                                                    >
                                                        {tag}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>

                                        {/* Active Filters */}
                                        {(selectedTags.length > 0 || selectedDifficulty !== "all" || searchTerm) && (
                                            <div className="space-y-2">
                                                <label className="text-sm font-medium">Active Filters</label>
                                                <div className="flex flex-wrap gap-1">
                                                    {searchTerm && (
                                                        <Badge variant="secondary" className="text-xs">
                                                            Search: {searchTerm}
                                                            <X
                                                                className="w-3 h-3 ml-1 cursor-pointer"
                                                                onClick={() => setSearchTerm("")}
                                                            />
                                                        </Badge>
                                                    )}
                                                    {selectedDifficulty !== "all" && (
                                                        <Badge variant="secondary" className="text-xs">
                                                            {selectedDifficulty}
                                                            <X
                                                                className="w-3 h-3 ml-1 cursor-pointer"
                                                                onClick={() => setSelectedDifficulty("all")}
                                                            />
                                                        </Badge>
                                                    )}
                                                    {selectedTags.map((tag) => (
                                                        <Badge key={tag} variant="secondary" className="text-xs">
                                                            {tag}
                                                            <X
                                                                className="w-3 h-3 ml-1 cursor-pointer"
                                                                onClick={() => toggleTag(tag)}
                                                            />
                                                        </Badge>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </Card>
                                )}

                                {/* Problems List */}
                                <div className="space-y-2">
                                    {filteredProblems.length > 0 ? (
                                        <>
                                            {filteredProblems.map((p) => (
                                                <Card
                                                    key={p.id}
                                                    className={`cursor-pointer transition-all hover:shadow-md ${selected?.id === p.id ? "border-primary shadow-md" : ""
                                                        }`}
                                                    onClick={() => setSelected(p)}
                                                >
                                                    <CardHeader className="p-4">
                                                        <div className="flex items-start justify-between gap-2">
                                                            <CardTitle className="text-base">{p.title}</CardTitle>
                                                            {selected?.id === p.id && (
                                                                <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0" />
                                                            )}
                                                        </div>
                                                        <div className="flex items-center gap-2 flex-wrap">
                                                            <Badge variant={getDifficultyVariant(p.difficulty)} className="w-fit">
                                                                {p.difficulty}
                                                            </Badge>
                                                            {p.tags && p.tags.slice(0, 2).map((tag) => (
                                                                <Badge key={tag} variant="outline" className="text-xs">
                                                                    {tag}
                                                                </Badge>
                                                            ))}
                                                            {p.tags && p.tags.length > 2 && (
                                                                <Badge variant="outline" className="text-xs">
                                                                    +{p.tags.length - 2}
                                                                </Badge>
                                                            )}
                                                        </div>
                                                    </CardHeader>
                                                </Card>
                                            ))}

                                            {/* Pagination Controls */}
                                            <div className="pt-4">
                                                <Pagination
                                                    currentPage={currentPage}
                                                    totalPages={totalPages}
                                                    onPageChange={handlePageChange}
                                                    totalItems={totalProblems}
                                                    itemsPerPage={problemsPerPage}
                                                />
                                            </div>
                                        </>
                                    ) : (
                                        <Card>
                                            <CardContent className="p-6 text-center">
                                                <Search className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                                                <p className="text-muted-foreground">No problems match your filters</p>
                                                <Button variant="outline" size="sm" className="mt-2" onClick={clearFilters}>
                                                    Clear Filters
                                                </Button>
                                            </CardContent>
                                        </Card>
                                    )}
                                </div>
                            </div>
                        </ScrollArea>
                    </div>
                )}

                {/* Middle - Problem Description & Results */}
                <div className={`${showSidebar ? "col-span-12 lg:col-span-4" : "col-span-12 lg:col-span-5"}`}>
                    <ScrollArea className="h-full">
                        <div className="p-6 space-y-6">
                            {selected ? (
                                <>
                                    {/* Problem Header */}
                                    <div>
                                        <h2 className="text-3xl font-bold mb-3">{selected.title}</h2>
                                        <div className="flex items-center gap-2 flex-wrap">
                                            <Badge variant={getDifficultyVariant(selected.difficulty)}>
                                                {selected.difficulty}
                                            </Badge>
                                            <Badge variant="outline">Problem #{selected.id}</Badge>
                                            {selected.tags && selected.tags.map((tag) => (
                                                <Badge key={tag} variant="secondary" className="text-xs">
                                                    <Tag className="w-3 h-3 mr-1" />
                                                    {tag}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Problem Description */}
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Description</CardTitle>
                                        </CardHeader>
                                        <CardContent className="overflow-hidden">
                                            <div className="prose prose-sm dark:prose-invert max-w-none overflow-x-auto">
                                                <ReactMarkdown
                                                    remarkPlugins={[remarkGfm]}
                                                    components={{
                                                        // Ensure code blocks don't break layout
                                                        pre: ({ node, ...props }) => (
                                                            <pre className="overflow-x-auto" {...props} />
                                                        ),
                                                        // Add proper spacing for paragraphs
                                                        p: ({ node, ...props }) => (
                                                            <p className="my-4" {...props} />
                                                        ),
                                                        // Style headings
                                                        h2: ({ node, ...props }) => (
                                                            <h2 className="mt-8 mb-4 text-xl font-semibold border-b pb-2" {...props} />
                                                        ),
                                                        h3: ({ node, ...props }) => (
                                                            <h3 className="mt-6 mb-3 text-lg font-semibold" {...props} />
                                                        ),
                                                    }}
                                                >
                                                    {selected.statement}
                                                </ReactMarkdown>
                                            </div>
                                        </CardContent>
                                    </Card>

                                    {/* Sample Testcases */}
                                    {testcases.filter((tc) => tc.is_sample).length > 0 && (
                                        <Card>
                                            <CardHeader>
                                                <div className="flex items-center justify-between">
                                                    <CardTitle>Sample Testcases</CardTitle>
                                                    <Badge>{testcases.filter((tc) => tc.is_sample).length}</Badge>
                                                </div>
                                            </CardHeader>
                                            <CardContent className="space-y-4">
                                                {testcases
                                                    .filter((tc) => tc.is_sample)
                                                    .map((tc, idx) => (
                                                        <div key={tc.id} className="space-y-2">
                                                            <div className="text-sm font-semibold">
                                                                {tc.description || `Sample ${idx + 1}`}
                                                            </div>
                                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                                                <div>
                                                                    <div className="text-xs text-muted-foreground mb-1">
                                                                        Input:
                                                                    </div>
                                                                    <pre className="text-sm bg-muted p-3 rounded-md font-mono overflow-x-auto">
                                                                        {tc.stdin || "(empty)"}
                                                                    </pre>
                                                                </div>
                                                                <div>
                                                                    <div className="text-xs text-muted-foreground mb-1">
                                                                        Expected Output:
                                                                    </div>
                                                                    <pre className="text-sm bg-muted p-3 rounded-md font-mono overflow-x-auto">
                                                                        {tc.expected_output}
                                                                    </pre>
                                                                </div>
                                                            </div>
                                                            {idx < testcases.filter((tc) => tc.is_sample).length - 1 && (
                                                                <Separator className="mt-4" />
                                                            )}
                                                        </div>
                                                    ))}
                                            </CardContent>
                                        </Card>
                                    )}

                                    {/* Submit Section */}
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Submit Solution</CardTitle>
                                            <CardDescription>Run your code against all test cases</CardDescription>
                                        </CardHeader>
                                        <CardContent>
                                            <Button onClick={submitCode} disabled={loading} className="w-full" size="lg">
                                                {loading ? (
                                                    <>
                                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                                                        Judging...
                                                    </>
                                                ) : (
                                                    <>
                                                        <Play className="w-4 h-4 mr-2" />
                                                        Run Code
                                                    </>
                                                )}
                                            </Button>
                                        </CardContent>
                                    </Card>

                                    {/* Submission Results */}
                                    {submissionResult && (
                                        <Card>
                                            <CardHeader>
                                                <div className="flex items-center justify-between">
                                                    <CardTitle>Results</CardTitle>
                                                    <Badge
                                                        variant={
                                                            submissionResult.status === "Accepted"
                                                                ? "default"
                                                                : "destructive"
                                                        }
                                                        className="flex items-center gap-1"
                                                    >
                                                        {getStatusIcon(submissionResult.status)}
                                                        {submissionResult.status}
                                                    </Badge>
                                                </div>
                                            </CardHeader>
                                            <CardContent className="space-y-4">
                                                {/* Metrics Grid */}
                                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">Score</CardDescription>
                                                            <CardTitle className="text-2xl">
                                                                {submissionResult.score?.toFixed(1) || 0}/100
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">
                                                                Sample Tests
                                                            </CardDescription>
                                                            <CardTitle className="text-2xl">
                                                                {submissionResult.sample_passed}/
                                                                {submissionResult.sample_total}
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">
                                                                Hidden Tests
                                                            </CardDescription>
                                                            <CardTitle className="text-2xl">
                                                                {submissionResult.hidden_passed}/
                                                                {submissionResult.hidden_total}
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">Overall</CardDescription>
                                                            <CardTitle className="text-2xl">
                                                                {submissionResult.passed_testcases}/
                                                                {submissionResult.total_testcases}
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                </div>

                                                {/* Execution Metrics */}
                                                <div className="grid grid-cols-2 gap-3">
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">
                                                                Execution Time
                                                            </CardDescription>
                                                            <CardTitle className="text-xl">
                                                                {submissionResult.execution_time}ms
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardDescription className="text-xs">
                                                                Memory Used
                                                            </CardDescription>
                                                            <CardTitle className="text-xl">
                                                                {submissionResult.memory_used
                                                                    ? `${submissionResult.memory_used.toFixed(2)} MB`
                                                                    : "N/A"}
                                                            </CardTitle>
                                                        </CardHeader>
                                                    </Card>
                                                </div>

                                                {/* Sample Test Results */}
                                                {submissionResult.sample_results &&
                                                    submissionResult.sample_results.length > 0 && (
                                                        <div className="space-y-2">
                                                            <h4 className="text-sm font-semibold">
                                                                Sample Testcase Results
                                                            </h4>
                                                            {submissionResult.sample_results.map((result, idx) => (
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
                                                                                Test {idx + 1}
                                                                            </span>
                                                                            <Badge
                                                                                variant={
                                                                                    result.status === "Passed"
                                                                                        ? "default"
                                                                                        : "destructive"
                                                                                }
                                                                            >
                                                                                {result.status}
                                                                            </Badge>
                                                                        </div>
                                                                        {result.status !== "Passed" && (
                                                                            <div className="mt-2 space-y-2 text-sm">
                                                                                <div>
                                                                                    <span className="text-muted-foreground">
                                                                                        Expected:
                                                                                    </span>
                                                                                    <pre className="mt-1 bg-muted p-2 rounded text-xs">
                                                                                        {result.expected_output}
                                                                                    </pre>
                                                                                </div>
                                                                                <div>
                                                                                    <span className="text-muted-foreground">
                                                                                        Got:
                                                                                    </span>
                                                                                    <pre className="mt-1 bg-muted p-2 rounded text-xs">
                                                                                        {result.actual_output}
                                                                                    </pre>
                                                                                </div>
                                                                            </div>
                                                                        )}
                                                                    </CardHeader>
                                                                </Card>
                                                            ))}
                                                        </div>
                                                    )}

                                                {/* Hidden Test Summary */}
                                                {submissionResult.hidden_total > 0 && (
                                                    <Card>
                                                        <CardHeader className="p-4">
                                                            <CardTitle className="text-sm">Hidden Tests</CardTitle>
                                                            <CardDescription>
                                                                Passed {submissionResult.hidden_passed} out of{" "}
                                                                {submissionResult.hidden_total} hidden test cases
                                                            </CardDescription>
                                                        </CardHeader>
                                                    </Card>
                                                )}

                                                <Button
                                                    variant="outline"
                                                    className="w-full"
                                                    onClick={() => navigate(`/submission/${submissionResult.id}`)}
                                                >
                                                    View Full Details
                                                </Button>
                                            </CardContent>
                                        </Card>
                                    )}
                                </>
                            ) : (
                                <Card>
                                    <CardHeader>
                                        <CardTitle>No Problem Selected</CardTitle>
                                        <CardDescription>Select a problem from the sidebar to get started</CardDescription>
                                    </CardHeader>
                                </Card>
                            )}
                        </div>
                    </ScrollArea>
                </div>

                {/* Right - Code Editor */}
                <div className={`${showSidebar ? "col-span-12 lg:col-span-5" : "col-span-12 lg:col-span-7"} border-l`}>
                    <div className="h-full flex flex-col">
                        <div className="p-4 border-b space-y-3">
                            <div className="flex items-center justify-between">
                                <h3 className="font-semibold">Code Editor</h3>
                                <Badge variant="outline" className="text-xs">
                                    {language === "python" ? "🐍 Python" : "⚡ C++"}
                                </Badge>
                            </div>
                            <div className="flex items-center gap-2">
                                <label className="text-sm font-medium">Language:</label>
                                <Select value={language} onValueChange={setLanguage}>
                                    <SelectTrigger className="w-[180px]">
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="python">🐍 Python</SelectItem>
                                        <SelectItem value="cpp">⚡ C++</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>
                        <div className="flex-1">
                            <Editor
                                height="100%"
                                language={language}
                                value={code}
                                onChange={(value) => setCode(value || "")}
                                theme="vs-dark"
                                options={{
                                    minimap: { enabled: false },
                                    fontSize: 14,
                                    lineNumbers: "on",
                                    scrollBeyondLastLine: false,
                                    automaticLayout: true,
                                }}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
