import type { TPost } from "@/types";

export const Post = ({ subject, received_on, body }: TPost) => (
	<div className="relative grid gap-1 text-sm">
		<div className="absolute top-1 left-0.5 z-10 aspect-square w-2 translate-x-[-29.5px] rounded-full bg-gray-900 dark:bg-gray-50">
		</div>
		<div className="font-medium">
			{new Date(received_on as string)?.toDateString()}
		</div>
		<div className="font-semibold">{subject}</div>
		<div className="grid gap-4">
			<div className="text-gray-500 dark:text-gray-400">{body}</div>
		</div>
	</div>
);
