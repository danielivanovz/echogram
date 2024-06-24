import { Post } from "@/components/post";
import type { TPost } from "@/types";

export function Timeline({ posts }: { posts: TPost[] }) {
	return (
		<div className="p-6 sm:p-10">
			<div className="relative grid gap-10 pl-6 after:absolute after:inset-y-0 after:left-0 after:w-px after:bg-gray-500/20 dark:after:bg-gray-400/20">
				{posts.map((post) => (
					<Post key={post.subject}
						received_on={post.received_on}
						subject={post.subject}
						body={post.body}
						email_id={post.email_id}
						user_id={post.user_id}
					/>
				))}
			</div>
		</div>
	);
}


