import * as React from "react";
import { cva } from "class-variance-authority";
import { cn } from "../../lib/utils";

const badgeVariants = cva(
    "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2",
    {
        variants: {
            variant: {
                default: "border-transparent shadow hover:opacity-80",
                secondary: "border-transparent hover:opacity-80",
                destructive: "border-transparent shadow hover:opacity-80",
                outline: "",
                success: "border-transparent",
                warning: "border-transparent",
                error: "border-transparent",
            },
        },
        defaultVariants: {
            variant: "default",
        },
    }
);

const variantStyles = {
    default: {
        backgroundColor: "var(--color-primary)",
        color: "var(--color-primary-foreground)",
    },
    secondary: {
        backgroundColor: "var(--color-secondary)",
        color: "var(--color-secondary-foreground)",
    },
    destructive: {
        backgroundColor: "var(--color-destructive)",
        color: "var(--color-destructive-foreground)",
    },
    outline: {
        color: "var(--color-foreground)",
    },
    success: {
        backgroundColor: "color-mix(in srgb, #10b981 10%, transparent)",
        color: "#34d399",
        borderColor: "color-mix(in srgb, #10b981 20%, transparent)",
    },
    warning: {
        backgroundColor: "color-mix(in srgb, #f59e0b 10%, transparent)",
        color: "#fbbf24",
        borderColor: "color-mix(in srgb, #f59e0b 20%, transparent)",
    },
    error: {
        backgroundColor: "color-mix(in srgb, #ef4444 10%, transparent)",
        color: "#f87171",
        borderColor: "color-mix(in srgb, #ef4444 20%, transparent)",
    },
};

function Badge({ className, variant = "default", style, ...props }) {
    return (
        <div
            className={cn(badgeVariants({ variant }), className)}
            style={{ ...variantStyles[variant], ...style }}
            {...props}
        />
    );
}

export { Badge, badgeVariants };
