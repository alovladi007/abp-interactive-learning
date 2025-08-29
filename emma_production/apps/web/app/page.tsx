import React from 'react';
import { Canvas } from '@/components/Canvas';
import { VoiceInput } from '@/components/VoiceInput';
import { Visualizer3D } from '@/components/Visualizer3D';
import { CollaborativeBoard } from '@/components/CollaborativeBoard';
import { LearningPath } from '@/components/LearningPath';

export default function EMMAInterface() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2">
            EMMA
          </h1>
          <p className="text-xl text-gray-200">
            Expert Multimodal & Math Assistant
          </p>
          <p className="text-sm text-gray-300 mt-2">
            Empowering learners and researchers with expert-level mathematical problem-solving
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Multimodal Input Panel */}
          <div className="lg:col-span-2 bg-white/10 backdrop-blur-lg rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">Input Your Problem</h2>
            
            {/* Text/LaTeX Input */}
            <div className="mb-4">
              <textarea
                className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-gray-300"
                placeholder="Type your question or LaTeX equation..."
                rows={3}
              />
            </div>

            {/* Canvas for Drawing */}
            <div className="mb-4">
              <Canvas />
            </div>

            {/* Voice Input */}
            <div className="mb-4">
              <VoiceInput />
            </div>

            {/* File Upload */}
            <div className="mb-4">
              <input
                type="file"
                accept="image/*,.pdf,.docx"
                className="text-white"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold">
                Solve Problem
              </button>
              <button className="px-6 py-3 bg-gradient-to-r from-green-600 to-teal-600 text-white rounded-lg font-semibold">
                Teach Me
              </button>
              <button className="px-6 py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg font-semibold">
                Prove It
              </button>
            </div>
          </div>

          {/* Features Panel */}
          <div className="space-y-4">
            {/* 3D Visualizer */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-4">
              <h3 className="text-lg font-bold text-white mb-2">3D Visualization</h3>
              <Visualizer3D />
            </div>

            {/* Learning Path */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-4">
              <h3 className="text-lg font-bold text-white mb-2">Your Learning Path</h3>
              <LearningPath />
            </div>

            {/* Collaborative Mode */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-4">
              <h3 className="text-lg font-bold text-white mb-2">Collaborate</h3>
              <CollaborativeBoard />
            </div>
          </div>
        </div>

        {/* Solution Display Area */}
        <div className="mt-8 bg-white/10 backdrop-blur-lg rounded-xl p-6">
          <h2 className="text-2xl font-bold text-white mb-4">Solution</h2>
          <div className="text-white">
            {/* Step-by-step solution will appear here */}
            <p>Your expert solution will appear here with:</p>
            <ul className="list-disc list-inside mt-2">
              <li>Step-by-step explanations</li>
              <li>Interactive visualizations</li>
              <li>Alternative methods</li>
              <li>Practice problems</li>
              <li>Related concepts</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
