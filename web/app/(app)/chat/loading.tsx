import { Skeleton } from "@/components/ui/skeleton";

export default function ChatLoading() {
  return (
    <div className="flex h-[calc(100vh-11rem)] flex-col gap-4">
      <div className="space-y-2">
        <Skeleton className="h-8 w-56" />
        <Skeleton className="h-4 w-80" />
      </div>
      <div className="flex flex-1 flex-col gap-3">
        <Skeleton className="h-12 w-3/4" />
        <Skeleton className="h-12 w-2/3 self-end" />
        <Skeleton className="h-12 w-4/5" />
        <Skeleton className="h-12 w-1/2 self-end" />
      </div>
      <Skeleton className="h-10 w-full" />
    </div>
  );
}
