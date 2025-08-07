"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Sparkles,
  Video,
  Wand2,
  Settings,
  Play,
  Download,
  Share2,
  Clock,
  DollarSign,
  AlertCircle,
  CheckCircle,
  Loader2,
  Upload,
  FileText,
  Image,
  Music,
  Mic,
  Zap,
  Layers,
  Film,
  ChevronRight,
} from "lucide-react"
import {
  VideoEngine,
  VideoQuality,
  AspectRatio,
  Resolution,
  StylePreset,
  ProjectStatus,
} from "@/types/video"

const engines = [
  {
    id: VideoEngine.SORA,
    name: "OpenAI Sora",
    description: "Best quality, up to 60s",
    icon: Sparkles,
    badge: "Premium",
    color: "from-purple-500 to-pink-500",
  },
  {
    id: VideoEngine.RUNWAY_GEN3,
    name: "Runway Gen-3",
    description: "Fast generation, 25s clips",
    icon: Zap,
    badge: "Popular",
    color: "from-blue-500 to-cyan-500",
  },
  {
    id: VideoEngine.LUMA_DREAM,
    name: "Luma Dream",
    description: "Stylized videos, 120fps",
    icon: Film,
    badge: "Creative",
    color: "from-orange-500 to-red-500",
  },
  {
    id: VideoEngine.ANIMATEDIFF,
    name: "AnimateDiff",
    description: "Open-source, customizable",
    icon: Layers,
    badge: "Free",
    color: "from-green-500 to-emerald-500",
  },
]

const stylePresets = [
  { id: StylePreset.CINEMATIC, name: "Cinematic", icon: "🎬" },
  { id: StylePreset.PHOTOREALISTIC, name: "Photorealistic", icon: "📸" },
  { id: StylePreset.ANIME, name: "Anime", icon: "🎌" },
  { id: StylePreset.CARTOON, name: "3D Cartoon", icon: "🎨" },
  { id: StylePreset.CYBERPUNK, name: "Cyberpunk", icon: "🤖" },
  { id: StylePreset.FANTASY, name: "Fantasy", icon: "🧙" },
  { id: StylePreset.WATERCOLOR, name: "Watercolor", icon: "🖌️" },
  { id: StylePreset.SKETCH, name: "Sketch", icon: "✏️" },
]

const aspectRatios = [
  { id: AspectRatio.SIXTEEN_NINE, name: "16:9", description: "Landscape" },
  { id: AspectRatio.NINE_SIXTEEN, name: "9:16", description: "Portrait" },
  { id: AspectRatio.ONE_ONE, name: "1:1", description: "Square" },
  { id: AspectRatio.TWENTY_ONE_NINE, name: "21:9", description: "Cinematic" },
]

export default function AIVideoGeneratorPage() {
  const [text, setText] = useState("")
  const [selectedEngine, setSelectedEngine] = useState(VideoEngine.SORA)
  const [selectedStyle, setSelectedStyle] = useState(StylePreset.CINEMATIC)
  const [selectedAspectRatio, setSelectedAspectRatio] = useState(AspectRatio.SIXTEEN_NINE)
  const [quality, setQuality] = useState(VideoQuality.HIGH)
  const [duration, setDuration] = useState(30)
  const [isGenerating, setIsGenerating] = useState(false)
  const [projectStatus, setProjectStatus] = useState<ProjectStatus | null>(null)

  const handleGenerate = async () => {
    if (!text.trim()) return
    
    setIsGenerating(true)
    setProjectStatus(ProjectStatus.SCRIPTING)
    
    // Simulate generation process
    setTimeout(() => {
      setProjectStatus(ProjectStatus.STORYBOARDING)
    }, 3000)
    
    setTimeout(() => {
      setProjectStatus(ProjectStatus.GENERATING)
    }, 6000)
    
    setTimeout(() => {
      setProjectStatus(ProjectStatus.POST_PROCESSING)
    }, 12000)
    
    setTimeout(() => {
      setProjectStatus(ProjectStatus.COMPLETED)
      setIsGenerating(false)
    }, 15000)
  }

  const getStatusIcon = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.SCRIPTING:
        return <FileText className="h-4 w-4" />
      case ProjectStatus.STORYBOARDING:
        return <Image className="h-4 w-4" />
      case ProjectStatus.GENERATING:
        return <Video className="h-4 w-4" />
      case ProjectStatus.POST_PROCESSING:
        return <Wand2 className="h-4 w-4" />
      case ProjectStatus.COMPLETED:
        return <CheckCircle className="h-4 w-4" />
      default:
        return <Loader2 className="h-4 w-4 animate-spin" />
    }
  }

  const getStatusMessage = (status: ProjectStatus) => {
    switch (status) {
      case ProjectStatus.SCRIPTING:
        return "Creating script from your text..."
      case ProjectStatus.STORYBOARDING:
        return "Generating storyboard frames..."
      case ProjectStatus.GENERATING:
        return "Creating video with AI..."
      case ProjectStatus.POST_PROCESSING:
        return "Enhancing quality and adding effects..."
      case ProjectStatus.COMPLETED:
        return "Your video is ready!"
      default:
        return "Processing..."
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <div className="text-center mb-12">
        <Badge variant="outline" className="mb-4">
          <Sparkles className="mr-1 h-3 w-3" />
          AI Video Generator
        </Badge>
        <h1 className="text-4xl font-bold mb-4">
          Transform Text into
          <span className="gradient-primary text-gradient"> Stunning Videos</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Powered by cutting-edge AI models including OpenAI Sora, Runway Gen-3, and more.
          Create professional videos in minutes.
        </p>
      </div>

      {/* Main Content */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column - Input and Settings */}
        <div className="lg:col-span-2 space-y-6">
          {/* Text Input */}
          <Card>
            <CardHeader>
              <CardTitle>Enter Your Text</CardTitle>
              <CardDescription>
                Describe what you want to create. Be specific about visuals, mood, and style.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="A serene sunrise over mountains with mist flowing through valleys, birds flying in formation..."
                className="w-full min-h-[150px] p-4 rounded-lg border bg-background resize-none focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <div className="flex items-center justify-between mt-4">
                <span className="text-sm text-muted-foreground">
                  {text.length} characters
                </span>
                <Button variant="outline" size="sm">
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Script
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Engine Selection */}
          <Card>
            <CardHeader>
              <CardTitle>Choose AI Engine</CardTitle>
              <CardDescription>
                Select the AI model that best fits your needs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                {engines.map((engine) => (
                  <button
                    key={engine.id}
                    onClick={() => setSelectedEngine(engine.id)}
                    className={`relative p-4 rounded-lg border-2 transition-all ${
                      selectedEngine === engine.id
                        ? "border-primary bg-primary/5"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    <div className={`absolute top-2 right-2 h-8 w-8 rounded-full bg-gradient-to-br ${engine.color} flex items-center justify-center`}>
                      <engine.icon className="h-4 w-4 text-white" />
                    </div>
                    <div className="text-left">
                      <h4 className="font-semibold">{engine.name}</h4>
                      <p className="text-sm text-muted-foreground mt-1">
                        {engine.description}
                      </p>
                      <Badge variant="secondary" className="mt-2">
                        {engine.badge}
                      </Badge>
                    </div>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Style Selection */}
          <Card>
            <CardHeader>
              <CardTitle>Visual Style</CardTitle>
              <CardDescription>
                Choose the artistic style for your video
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-3">
                {stylePresets.map((style) => (
                  <button
                    key={style.id}
                    onClick={() => setSelectedStyle(style.id)}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      selectedStyle === style.id
                        ? "border-primary bg-primary/5"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    <div className="text-2xl mb-1">{style.icon}</div>
                    <div className="text-xs font-medium">{style.name}</div>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Advanced Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Advanced Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Aspect Ratio */}
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Aspect Ratio
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {aspectRatios.map((ratio) => (
                    <button
                      key={ratio.id}
                      onClick={() => setSelectedAspectRatio(ratio.id)}
                      className={`p-2 rounded-md border text-sm transition-all ${
                        selectedAspectRatio === ratio.id
                          ? "border-primary bg-primary/5"
                          : "border-border hover:border-primary/50"
                      }`}
                    >
                      <div className="font-medium">{ratio.name}</div>
                      <div className="text-xs text-muted-foreground">
                        {ratio.description}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Duration */}
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Duration: {duration}s
                </label>
                <input
                  type="range"
                  min="5"
                  max="60"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Quality */}
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Quality
                </label>
                <div className="flex gap-2">
                  {Object.values(VideoQuality).map((q) => (
                    <Button
                      key={q}
                      variant={quality === q ? "default" : "outline"}
                      size="sm"
                      onClick={() => setQuality(q)}
                    >
                      {q.charAt(0).toUpperCase() + q.slice(1)}
                    </Button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Preview and Actions */}
        <div className="space-y-6">
          {/* Cost Estimate */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Cost Estimate
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Video Generation</span>
                  <span className="font-medium">$2.50</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Voice Over</span>
                  <span className="font-medium">$0.50</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Music</span>
                  <span className="font-medium">$0.30</span>
                </div>
                <div className="border-t pt-2 flex justify-between">
                  <span className="font-medium">Total</span>
                  <span className="font-bold text-lg">$3.30</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-4">
                Or use 33 credits from your subscription
              </p>
            </CardContent>
          </Card>

          {/* Generate Button */}
          <Button
            size="lg"
            className="w-full"
            variant="gradient"
            onClick={handleGenerate}
            disabled={!text.trim() || isGenerating}
          >
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-5 w-5" />
                Generate Video
              </>
            )}
          </Button>

          {/* Status Card */}
          {projectStatus && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {getStatusIcon(projectStatus)}
                  Generation Progress
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm mb-4">{getStatusMessage(projectStatus)}</p>
                <div className="space-y-2">
                  {[
                    ProjectStatus.SCRIPTING,
                    ProjectStatus.STORYBOARDING,
                    ProjectStatus.GENERATING,
                    ProjectStatus.POST_PROCESSING,
                    ProjectStatus.COMPLETED,
                  ].map((status) => (
                    <div
                      key={status}
                      className={`flex items-center gap-2 text-sm ${
                        projectStatus === status
                          ? "text-primary font-medium"
                          : projectStatus > status
                          ? "text-muted-foreground line-through"
                          : "text-muted-foreground/50"
                      }`}
                    >
                      {projectStatus >= status ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : projectStatus === status ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <div className="h-4 w-4 rounded-full border-2" />
                      )}
                      {status.replace(/_/g, " ").toLowerCase()}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Preview */}
          {projectStatus === ProjectStatus.COMPLETED && (
            <Card>
              <CardHeader>
                <CardTitle>Preview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-video bg-gradient-to-br from-primary/20 to-secondary/20 rounded-lg flex items-center justify-center mb-4">
                  <Play className="h-12 w-12 text-primary" />
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Download className="mr-2 h-4 w-4" />
                    Download
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Share2 className="mr-2 h-4 w-4" />
                    Share
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5" />
                Pro Tips
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <ChevronRight className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  Be specific about camera movements and visual details
                </li>
                <li className="flex items-start gap-2">
                  <ChevronRight className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  Include emotional tone and pacing in your description
                </li>
                <li className="flex items-start gap-2">
                  <ChevronRight className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  Reference specific styles or films for better results
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}