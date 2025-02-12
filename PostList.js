import React, { useState } from "react";
import { QueryClient, QueryClientProvider, useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

const queryClient = new QueryClient();

const fetchPosts = async () => {
  const { data } = await axios.get("https://jsonplaceholder.typicode.com/posts");
  return data;
};

const createPost = async (newPost) => {
  const { data } = await axios.post("https://jsonplaceholder.typicode.com/posts", newPost);
  return data;
};

const updatePost = async (post) => {
  const { data } = await axios.put(`https://jsonplaceholder.typicode.com/posts/${post.id}`, post);
  return data;
};

const deletePost = async (id) => {
  await axios.delete(`https://jsonplaceholder.typicode.com/posts/${id}`);
  return id;
};

const PostList = () => {
  const queryClient = useQueryClient();
  const { data: posts, isLoading, error } = useQuery({ queryKey: ["posts"], queryFn: fetchPosts });

  const mutationCreate = useMutation({
    mutationFn: createPost,
    onSuccess: () => queryClient.invalidateQueries("posts"),
  });

  const mutationUpdate = useMutation({
    mutationFn: updatePost,
    onSuccess: () => queryClient.invalidateQueries("posts"),
  });

  const mutationDelete = useMutation({
    mutationFn: deletePost,
    onSuccess: () => queryClient.invalidateQueries("posts"),
  });

  const [newPost, setNewPost] = useState({ title: "", body: "" });

  if (isLoading) return <p>Loading posts...</p>;
  if (error) return <p>Error fetching posts!</p>;

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold">Posts</h1>
      <input className="border p-2 w-full my-2" placeholder="Title" value={newPost.title} onChange={(e) => setNewPost({ ...newPost, title: e.target.value })} />
      <textarea className="border p-2 w-full my-2" placeholder="Body" value={newPost.body} onChange={(e) => setNewPost({ ...newPost, body: e.target.value })} />
      <button className="bg-blue-500 text-white p-2 w-full" onClick={() => mutationCreate.mutate(newPost)}>Create Post</button>
      {posts.map((post) => (
        <div key={post.id} className="border p-4 my-2">
          <h2 className="font-bold">{post.title}</h2>
          <p>{post.body}</p>
          <button className="bg-yellow-500 text-white p-2 mx-1" onClick={() => mutationUpdate.mutate({ ...post, title: "Updated Title" })}>Edit</button>
          <button className="bg-red-500 text-white p-2 mx-1" onClick={() => mutationDelete.mutate(post.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <PostList />
  </QueryClientProvider>
);

export default App;
