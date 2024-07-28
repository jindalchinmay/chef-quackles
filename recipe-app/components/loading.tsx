import React from 'react';
import { Coffee } from "lucide-react";

export default function Loading() {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center justify-center">
          Chef Quackles
        </h1>
        <p className="text-lg text-gray-600">
          Discovering duckalicious recipes...
        </p>
      </header>
      <div className="flex flex-col items-center">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Loading</h2>
        <span className="loading loading-dots loading-lg bg-green-500"></span>
      </div>
    </div>
  );
}