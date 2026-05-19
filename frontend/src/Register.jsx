import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authAPI } from "./utils/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ThemeToggle } from "@/components/theme-toggle";
import { Code, Mail, Lock, User, Eye, EyeOff, Loader2, CheckCircle2, ArrowRight, Sparkles, Users, Trophy, Check } from "lucide-react";

export default function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [msg, setMsg] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    // Password strength indicator
    const getPasswordStrength = () => {
        if (!password) return { strength: 0, label: "", color: "" };

        let strength = 0;
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;

        if (strength <= 1) return { strength: 1, label: "Weak", color: "bg-red-500" };
        if (strength <= 3) return { strength: 2, label: "Fair", color: "bg-yellow-500" };
        if (strength <= 4) return { strength: 3, label: "Good", color: "bg-blue-500" };
        return { strength: 4, label: "Strong", color: "bg-green-500" };
    };

    const passwordStrength = getPasswordStrength();

    const register = async () => {
        if (!name || !email || !password) {
            setMsg("Please fill in all fields");
            return;
        }

        if (password.length < 6) {
            setMsg("Password must be at least 6 characters");
            return;
        }

        try {
            setLoading(true);
            setMsg("");
            await authAPI.signup({ name, email, password });

            setSuccess(true);
            setTimeout(() => navigate("/login"), 1500);
        } catch (err) {
            setMsg(err.response?.data?.detail || "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            register();
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
                                Start Your
                                <br />
                                <span className="text-primary">Coding Journey</span>
                            </h1>
                            <p className="text-xl text-muted-foreground max-w-md">
                                Join thousands of developers improving their skills through practice and collaboration.
                            </p>
                        </div>

                        {/* Features */}
                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Trophy className="w-5 h-5 text-primary" />
                                </div>
                                <div>
                                    <div className="font-semibold text-foreground">100+ Problems</div>
                                    <div className="text-sm">From easy to expert level</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Users className="w-5 h-5 text-primary" />
                                </div>
                                <div>
                                    <div className="font-semibold text-foreground">Real-time Collaboration</div>
                                    <div className="text-sm">Code together with peers</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-3 text-muted-foreground">
                                <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                                    <Sparkles className="w-5 h-5 text-primary" />
                                </div>
                                <div>
                                    <div className="font-semibold text-foreground">AI Feedback</div>
                                    <div className="text-sm">Get instant code reviews</div>
                                </div>
                            </div>
                        </div>

                        {/* Stats */}
                        <div className="flex gap-8 pt-8 border-t border-border">
                            <div>
                                <div className="text-3xl font-bold text-primary">10K+</div>
                                <div className="text-sm text-muted-foreground">Active Users</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-primary">50K+</div>
                                <div className="text-sm text-muted-foreground">Solutions</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-primary">100+</div>
                                <div className="text-sm text-muted-foreground">Problems</div>
                            </div>
                        </div>
                    </div>

                    {/* Footer */}
                    <div className="text-sm text-muted-foreground">
                        © 2024 CodeJudge. All rights reserved.
                    </div>
                </div>
            </div>

            {/* Right Side - Register Form */}
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

                    {/* Register Card */}
                    <Card className="border-2">
                        <CardHeader className="space-y-1">
                            <CardTitle className="text-2xl">Create an account</CardTitle>
                            <CardDescription>Enter your details to get started</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {/* Name Input */}
                            <div className="space-y-2">
                                <Label htmlFor="name">Full Name</Label>
                                <div className="relative">
                                    <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        id="name"
                                        type="text"
                                        placeholder="John Doe"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        className="pl-10"
                                        autoComplete="name"
                                    />
                                </div>
                            </div>

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
                                <Label htmlFor="password">Password</Label>
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
                                        autoComplete="new-password"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-3 text-muted-foreground hover:text-foreground transition-colors"
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>

                                {/* Password Strength Indicator */}
                                {password && (
                                    <div className="space-y-2">
                                        <div className="flex gap-1">
                                            {[1, 2, 3, 4].map((level) => (
                                                <div
                                                    key={level}
                                                    className={`h-1 flex-1 rounded-full transition-colors ${level <= passwordStrength.strength
                                                            ? passwordStrength.color
                                                            : "bg-muted"
                                                        }`}
                                                />
                                            ))}
                                        </div>
                                        <p className="text-xs text-muted-foreground">
                                            Password strength: <span className="font-semibold">{passwordStrength.label}</span>
                                        </p>
                                    </div>
                                )}

                                <div className="space-y-1 text-xs text-muted-foreground">
                                    <div className="flex items-center gap-2">
                                        <Check className={`h-3 w-3 ${password.length >= 6 ? 'text-green-500' : 'text-muted-foreground'}`} />
                                        <span>At least 6 characters</span>
                                    </div>
                                </div>
                            </div>

                            {/* Error Message */}
                            {msg && (
                                <Alert variant="destructive">
                                    <AlertDescription>{msg}</AlertDescription>
                                </Alert>
                            )}

                            {/* Success Message */}
                            {success && (
                                <Alert className="border-green-500 bg-green-500/10">
                                    <CheckCircle2 className="h-4 w-4 text-green-500" />
                                    <AlertDescription className="text-green-500">
                                        Account created! Redirecting to login...
                                    </AlertDescription>
                                </Alert>
                            )}

                            {/* Register Button */}
                            <Button
                                onClick={register}
                                disabled={loading || success}
                                className="w-full"
                                size="lg"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Creating account...
                                    </>
                                ) : success ? (
                                    <>
                                        <CheckCircle2 className="mr-2 h-4 w-4" />
                                        Success!
                                    </>
                                ) : (
                                    <>
                                        Create Account
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </Button>

                            {/* Terms */}
                            <p className="text-xs text-center text-muted-foreground">
                                By creating an account, you agree to our{" "}
                                <button className="text-primary hover:underline">Terms of Service</button>
                                {" "}and{" "}
                                <button className="text-primary hover:underline">Privacy Policy</button>
                            </p>
                        </CardContent>
                        <CardFooter className="flex flex-col space-y-4">
                            <div className="relative w-full">
                                <div className="absolute inset-0 flex items-center">
                                    <span className="w-full border-t" />
                                </div>
                                <div className="relative flex justify-center text-xs uppercase">
                                    <span className="bg-card px-2 text-muted-foreground">
                                        Already have an account?
                                    </span>
                                </div>
                            </div>
                            <Button variant="outline" className="w-full" asChild>
                                <Link to="/login">
                                    Sign in instead
                                </Link>
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            </div>
        </div>
    );
}
