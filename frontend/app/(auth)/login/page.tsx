"use client";
import { useState } from "react";
import { login } from "@/services/auth.service";
import { useRouter } from "next/navigation";

export default function LoginPage() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const router = useRouter();

    async function handleSubmit(
        e: React.FormEvent
    ) {
        e.preventDefault();

    try {
            const response = await login(
                email,
                password
            );

            router.push("/dashboard");

        } catch (error) {
            setError("Email ou mot de passe incorrect");
        }
    }

    return (
    <main>
        <form onSubmit={handleSubmit}>
            <h1>
                Login
            </h1>

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">
                Se connecter
            </button>
        </form>
        {error && (
            <p>
                {error}
            </p>
        )}
    </main>
);
}