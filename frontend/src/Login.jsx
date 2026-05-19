import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI, setAuthToken, setUser } from "./utils/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ThemeToggle } from "@/components/theme-toggle";
import { Code, Mail, Lock, Eye, EyeOff, Loader2, ArrowRight, Sparkles, Users, Trophy } from "lucide-react";

export default function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [msg, setMsg] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const login = async () => {
        if (!email || !password) {
            setMsg("Please fill in all fields");
            return;
        }

        try {
            setLoading(true);
            setMsg("");

            const res = await authAPI.login({ email, password });
            setAuthToken(res.data.access_token);
            setUser(res.data.user);

            window.location.href = "/judge";
        } catch (err) {
            console.error("Login error:", err);
            setMsg(err?.response?.data?.detail || "Invalid email or password");
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            login();
        }
    };

    return (
        <div className="min-h-screen bg-background flex">
            {/* Left Side - Hero Section */}
            <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary/10 via-primary/5 to-background relative overflow-hidden">
                <div className="absolute inset-0 bg-grid-white/5 [mask-image:radial-gradient(white,transparent_85%)]" />

                <div className="relative z-10 flex flex-col justify-between p-12 w-full">
                    {/* Logo */}
                    <div className="flex items-center gap-3">
                        <div className="flex items-center justify-center w-12 h-12 rounded-xl bg-primary">
                            <Code className="w-6 h-6 text-primary-foreground" />
                        </div>
                        <span className="text-2xl font-bold">CodeJudge</span>
                    </div>

                    {/* Hero Content */}
                    <div className="space-y-8">
                        <div className="space-y-4">
                            <h1 className="text-5xl font-bold leading-tight">
                                Master Coding
                                <br />
                                <span className="text-primary">Together</span>
                            </h1>
                            <p className="text-xl text-muted-foreground max-w-md">
                                Practice algorithms, compete with peers, and collaborate in real-time coding rooms.
                            </p>
                        </div>

                        {/* Features */}
                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Trophy className="w-5 h-5 text-primary" />
                                </div>
                                <span>Solve 100+ coding challenges</span>
                            </div>
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Users className="w-5 h-5 text-primary" />
                                </div>
                                <span>Collaborate in real-time rooms</span>
                            </div>
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Sparkles className="w-5 h-5 text-primary" />
                                </div>
                                <span>Get AI-powered feedback</span>
                            </div>
                        </div>
                    </div>

                    {/* Footer */}
                    <div className="text-sm text-muted-foreground">
                        © 2026 CodeJudge. All rights reserved.
                    </div>
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
                <div className="w-full max-w-md space-y-8">
                    {/* Theme Toggle */}
                    <div className="flex justify-end">
                        <ThemeToggle />
                    </div>

                    {/* Mobile Logo */}
                    <div className="lg:hidden text-center space-y-2">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary mb-4">
                            <Code className="w-8 h-8 text-primary-foreground" />
                        </div>
                        <h1 className="text-3xl font-bold">CodeJudge</h1>
                    </div>

                    {/* Login Card */}
                    <Card className="border-2">
                        <CardHeader className="space-y-1">
                            <CardTitle className="text-2xl">Welcome back</CardTitle>
                            <CardDescription>Sign in to your account to continue</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {/* Email Input */}
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        id="email"
                                        type="email"
                                        placeholder="you@example.com"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        className="pl-10"
                                        autoComplete="email"
                                    />
                                </div>
                            </div>

                            {/* Password Input */}
                            <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <Label htmlFor="password">Password</Label>
                                    <button className="text-xs text-primary hover:underline">
                                        Forgot password?
                                    </button>
                                </div>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        id="password"
                                        type={showPassword ? "text" : "password"}
                                        placeholder="••••••••"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        className="pl-10 pr-10"
                                        autoComplete="current-password"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-3 text-muted-foreground hover:text-foreground transition-colors"
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                            </div>

                            {/* Error Message */}
                            {msg && (
                                <Alert variant="destructive">
                                    <AlertDescription>{msg}</AlertDescription>
                                </Alert>
                            )}

                            {/* Login Button */}
                            <Button onClick={login} disabled={loading} className="w-full" size="lg">
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Signing in...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </Button>
                        </CardContent>
                        <CardFooter className="flex flex-col space-y-4">
                            <div className="relative w-full">
                                <div className="absolute inset-0 flex items-center">
                                    <span className="w-full border-t" />
                                </div>
                                <div className="relative flex justify-center text-xs uppercase">
                                    <span className="bg-card px-2 text-muted-foreground">
                                        New to CodeJudge?
                                    </span>
                                </div>
                            </div>
                            <Button variant="outline" className="w-full" asChild>
                                <Link to="/signup">
                                    Create an account
                                </Link>
                            </Button>
                        </CardFooter>
                    </Card>

                    {/* Footer */}
                    <p className="text-center text-xs text-muted-foreground">
                        Secure authentication powered by JWT
                    </p>
                </div>
            </div>
        </div>
    );
}
