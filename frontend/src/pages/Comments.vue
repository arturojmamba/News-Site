<template>
    <div>
        <h2 class="mb-4">Comments</h2>
        <div class="input-group mb-3">
            <textarea class="form-control" v-model="newComment" placeholder="Write a comment..."></textarea>
            <button class="btn btn-primary" @click="submitComment">Post Comment</button>
        </div>

        <div v-for="comment in comments" :key="comment.id" class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{{ comment.content }}</h5>
                <p class="card-text">By {{ comment.author__email }}</p>

                <!-- Reply Section -->
                <div v-if="comment.isReplying">
                    <textarea class="form-control" v-model="comment.replyContent" placeholder="Write a reply..."></textarea>
                    <button class="btn btn-success" @click="submitReply(comment)">Post Reply</button>
                    <button class="btn btn-secondary" @click="cancelReplying(comment)">Cancel</button>
                </div>
                <button class="btn btn-info" v-else @click="prepareReply(comment)">Reply</button>

                <!-- Edit and Delete Buttons for owned comments -->
                <div v-if="comment.author__email === userId?.email" class="mt-2">
                    <button class="btn btn-warning" @click="startEditing(comment)">Edit</button>
                    <button class="btn btn-danger" @click="deleteComment(comment.id)">Delete</button>
                </div>

                <!-- Comment Editing Section -->
                <div v-if="comment.isEditing">
                    <textarea class="form-control" v-model="comment.editedContent"></textarea>
                    <button class="btn btn-success" @click="updateComment(comment.id, comment.editedContent)">Save</button>
                    <button class="btn btn-secondary" @click="cancelEditing(comment)">Cancel</button>
                </div>

                <div v-for="reply in comment.replies" :key="reply.id" class="card mt-2 ml-4">
                    <div class="card-body">
                        <h6 class="card-title">{{ reply.content }}</h6>
                        <p class="card-text">By {{ reply.author__email }}</p>

                        <!-- Reply Editing Section -->
                        <div v-if="reply.isEditing">
                            <textarea class="form-control" v-model="reply.editedContent"></textarea>
                            <button class="btn btn-success" @click="updateComment(reply.id, reply.editedContent, 'reply')">Save</button>
                            <button class="btn btn-secondary" @click="cancelEditingReply(reply)">Cancel</button>
                        </div>

                        <!-- Edit and Delete Buttons for owned replies -->
                        <div v-if="reply.author__email === userId?.email" class="mt-2">
                            <button class="btn btn-warning" @click="startEditingReply(reply)">Edit</button>
                            <button class="btn btn-danger" @click="deleteComment(reply.id, 'reply')">Delete</button>
                        </div>
                    </div>
                    <div class="card-footer text-muted">
                        Posted on: {{ formatDate(reply.uploaded) }}
                    </div>
                </div>


            </div>
            <div class="card-footer text-muted">
                Posted on: {{ formatDate(comment.uploaded) }}
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { storeMe } from '../storage/userDetails';

export default defineComponent({
    props: {
        articleId: {
            type: Number,
            required: true
        },
        csrfToken: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const userStore = storeMe();
        const userId = ref(userStore.getCurrentUser);
        const newComment = ref('');
        const comments = ref([]);
        const csrfTokenCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

        onMounted(fetchComments);

        async function fetchComments() {
            try {
                const response = await fetch(`http://127.0.0.1:8000/articles/${props.articleId}/comments/`);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const fetchedComments = (await response.json()).comments;
                comments.value = fetchedComments.map(c => ({ ...c, isReplying: false, replyContent: '', isEditing: false, editedContent: '' }));

                console.log(userId)
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        }

        async function submitComment() {
            try {
                const response = await fetch(`http://127.0.0.1:8000/articles/${props.articleId}/comments/add/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfTokenCookie,
                    },
                    body: JSON.stringify({ content: newComment.value })
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                newComment.value = '';
                await fetchComments();
            } catch (error) {
                console.error('Error submitting comment:', error);
            }
        }

        function prepareReply(comment) {
            comment.isReplying = true;
        }

        function cancelReplying(comment) {
            comment.isReplying = false;
            comment.replyContent = '';
        }

        async function submitReply(comment) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/articles/${props.articleId}/comments/add/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfTokenCookie,
                    },
                    body: JSON.stringify({ content: comment.replyContent, parent_id: comment.id })
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                comment.replyContent = '';
                comment.isReplying = false;
                await fetchComments();
            } catch (error) {
                console.error('Error submitting reply:', error);
            }
        }

        function startEditing(comment) {
            comment.isEditing = true;
            comment.editedContent = comment.content;
        }

        function cancelEditing(comment) {
            comment.isEditing = false;
            comment.editedContent = '';
        }

        function startEditingReply(reply) {
            reply.isEditing = true;
            reply.editedContent = reply.content;
        }

        function cancelEditingReply(reply) {
            reply.isEditing = false;
            reply.editedContent = '';
        }

        async function updateComment(commentId, content) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/comments/${commentId}/update/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfTokenCookie,
                    },
                    body: JSON.stringify({ content })
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                await fetchComments();
            } catch (error) {
                console.error('Error updating comment:', error);
            }
        }

        async function deleteComment(commentId) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/comments/${commentId}/delete/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfTokenCookie,
                    }
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                await fetchComments();
            } catch (error) {
                console.error('Error deleting comment:', error);
            }
        }

        function formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        }

        return {
            newComment,
            comments,
            userId,
            submitComment,
            prepareReply,
            cancelReplying,
            submitReply,
            startEditing,
            cancelEditing,
            updateComment,
            deleteComment,
            startEditingReply,
            cancelEditingReply,
            formatDate
        };
    }
});
</script>
