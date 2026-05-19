import { cn } from "../../lib/utils";

function Skeleton({ className, style, ...props }) {
    return (
        <div
            className={cn("animate-pulse rounded-md", className)}
            style={{ backgroundColor: "var(--color-muted)", ...style }}
            {...props}
        />
    );
}

export { Skeleton };
