'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { TraceViewer } from '@/components/trace/TraceViewer';
import { FileUploader } from '@/components/upload/FileUploader';
import { CitationList } from '@/components/citations/CitationList';
import { useSolveStore } from '@/store/solve';
import { useAuthStore } from '@/store/auth';

export default function HomePage() {
  const [activeTab, setActiveTab] = useState('chat');
  const { currentRun, isLoading } = useSolveStore();
  const { user } = useAuthStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto p-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">
            EMMA - Expert Multimodal & Math Assistant
          </h1>
          <p className="text-gray-300">
            Advanced AI system for solving complex mathematical and scientific problems
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Chat & Input */}
          <div className="lg:col-span-2">
            <Card className="bg-white/10 backdrop-blur-lg border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Problem Solver</CardTitle>
                <CardDescription className="text-gray-300">
                  Enter your problem or upload documents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="chat">Chat</TabsTrigger>
                    <TabsTrigger value="upload">Upload</TabsTrigger>
                  </TabsList>
                  <TabsContent value="chat" className="mt-4">
                    <ChatInterface />
                  </TabsContent>
                  <TabsContent value="upload" className="mt-4">
                    <FileUploader />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* Right Panel - Results & Trace */}
          <div className="space-y-6">
            {/* Trace Viewer */}
            {currentRun && (
              <Card className="bg-white/10 backdrop-blur-lg border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Execution Trace</CardTitle>
                  <CardDescription className="text-gray-300">
                    Step-by-step solution process
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <TraceViewer runId={currentRun.id} />
                </CardContent>
              </Card>
            )}

            {/* Citations */}
            {currentRun?.citations && currentRun.citations.length > 0 && (
              <Card className="bg-white/10 backdrop-blur-lg border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Citations</CardTitle>
                  <CardDescription className="text-gray-300">
                    Sources and references
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <CitationList citations={currentRun.citations} />
                </CardContent>
              </Card>
            )}

            {/* Quick Stats */}
            <Card className="bg-white/10 backdrop-blur-lg border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Session Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-gray-300">
                  <div className="flex justify-between">
                    <span>Problems Solved:</span>
                    <span className="font-semibold">12</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg. Time:</span>
                    <span className="font-semibold">3.2s</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Accuracy:</span>
                    <span className="font-semibold">98.5%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}