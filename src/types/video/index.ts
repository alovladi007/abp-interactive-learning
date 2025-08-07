// Video Generation Types
export interface VideoProject {
  id: string
  userId: string
  title: string
  description?: string
  status: ProjectStatus
  createdAt: Date
  updatedAt: Date
  script?: VideoScript
  storyboard?: Storyboard
  settings: VideoSettings
  outputs?: VideoOutput[]
  metadata: ProjectMetadata
}

export enum ProjectStatus {
  DRAFT = 'draft',
  SCRIPTING = 'scripting',
  STORYBOARDING = 'storyboarding',
  GENERATING = 'generating',
  POST_PROCESSING = 'post_processing',
  QUALITY_CHECK = 'quality_check',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface VideoScript {
  id: string
  projectId: string
  rawText: string
  beats: ScriptBeat[]
  duration: number
  voiceOver?: VoiceOverConfig
  music?: MusicConfig
}

export interface ScriptBeat {
  id: string
  beatNumber: number
  logline: string
  voText: string
  emotion: EmotionKeyword
  visualHook: VisualHook
  duration: number
  timestamp: number
}

export enum EmotionKeyword {
  EXCITED = 'excited',
  CALM = 'calm',
  DRAMATIC = 'dramatic',
  MYSTERIOUS = 'mysterious',
  HAPPY = 'happy',
  SAD = 'sad',
  TENSE = 'tense',
  ROMANTIC = 'romantic'
}

export interface VisualHook {
  camera: CameraMovement
  subject: string
  style?: string
  lighting?: string
}

export enum CameraMovement {
  STATIC = 'static',
  PAN_LEFT = 'pan_left',
  PAN_RIGHT = 'pan_right',
  ZOOM_IN = 'zoom_in',
  ZOOM_OUT = 'zoom_out',
  DOLLY_IN = 'dolly_in',
  DOLLY_OUT = 'dolly_out',
  TRACKING = 'tracking',
  AERIAL = 'aerial'
}

export interface Storyboard {
  id: string
  projectId: string
  frames: StoryboardFrame[]
}

export interface StoryboardFrame {
  id: string
  beatId: string
  prompt: string
  negativePrompt?: string
  seed: string
  imageUrl?: string
  thumbnailUrl?: string
  metadata: FrameMetadata
}

export interface FrameMetadata {
  style: string
  lighting: string
  colorGrade: string
  aspectRatio: AspectRatio
  resolution: Resolution
}

export enum AspectRatio {
  SIXTEEN_NINE = '16:9',
  NINE_SIXTEEN = '9:16',
  ONE_ONE = '1:1',
  FOUR_THREE = '4:3',
  TWENTY_ONE_NINE = '21:9'
}

export enum Resolution {
  SD = '480p',
  HD = '720p',
  FHD = '1080p',
  UHD = '4K',
  EIGHT_K = '8K'
}

export interface VideoSettings {
  engine: VideoEngine
  quality: VideoQuality
  fps: number
  aspectRatio: AspectRatio
  resolution: Resolution
  style: VideoStyle
  duration: number
  watermark: boolean
}

export enum VideoEngine {
  SORA = 'sora',
  RUNWAY_GEN3 = 'runway_gen3',
  LUMA_DREAM = 'luma_dream',
  ANIMATEDIFF = 'animatediff',
  VIDEOCRAFTER = 'videocrafter',
  STABLE_VIDEO = 'stable_video'
}

export enum VideoQuality {
  DRAFT = 'draft',
  STANDARD = 'standard',
  HIGH = 'high',
  ULTRA = 'ultra'
}

export interface VideoStyle {
  name: string
  preset?: StylePreset
  customPrompt?: string
  referenceImages?: string[]
}

export enum StylePreset {
  CINEMATIC = 'cinematic',
  ANIME = 'anime',
  PHOTOREALISTIC = 'photorealistic',
  CARTOON = 'cartoon',
  WATERCOLOR = 'watercolor',
  OIL_PAINTING = 'oil_painting',
  SKETCH = 'sketch',
  CYBERPUNK = 'cyberpunk',
  FANTASY = 'fantasy'
}

export interface VoiceOverConfig {
  provider: VoiceProvider
  voiceId: string
  emotion: string
  speed: number
  stability: number
  similarityBoost: number
  text: string
  audioUrl?: string
}

export enum VoiceProvider {
  ELEVENLABS = 'elevenlabs',
  OPENAI = 'openai',
  GOOGLE = 'google',
  AZURE = 'azure',
  CUSTOM = 'custom'
}

export interface MusicConfig {
  provider: MusicProvider
  genre: string
  mood: string
  tempo: number
  duration: number
  instrumental: boolean
  audioUrl?: string
}

export enum MusicProvider {
  SUNO = 'suno',
  MUSICGEN = 'musicgen',
  SOUNDRAW = 'soundraw',
  CUSTOM = 'custom'
}

export interface VideoOutput {
  id: string
  projectId: string
  type: OutputType
  url: string
  thumbnailUrl?: string
  duration: number
  fileSize: number
  format: VideoFormat
  metadata: OutputMetadata
  createdAt: Date
}

export enum OutputType {
  PREVIEW = 'preview',
  DRAFT = 'draft',
  FINAL = 'final',
  CLIP = 'clip'
}

export enum VideoFormat {
  MP4 = 'mp4',
  WEBM = 'webm',
  MOV = 'mov',
  AVI = 'avi',
  MKV = 'mkv'
}

export interface OutputMetadata {
  width: number
  height: number
  fps: number
  bitrate: number
  codec: string
  audioCodec?: string
  audioBitrate?: number
}

export interface ProjectMetadata {
  tags: string[]
  category: string
  visibility: 'public' | 'private' | 'unlisted'
  license: string
  credits: Credits
  analytics?: VideoAnalytics
}

export interface Credits {
  producer: string
  scriptWriter?: string
  voiceActor?: string
  musician?: string
  additionalCredits?: string[]
}

export interface VideoAnalytics {
  views: number
  likes: number
  shares: number
  watchTime: number
  completionRate: number
  engagement: number
}

// Pipeline Types
export interface PipelineTask {
  id: string
  type: TaskType
  status: TaskStatus
  progress: number
  startTime?: Date
  endTime?: Date
  error?: string
  result?: any
}

export enum TaskType {
  SCRIPT_GENERATION = 'script_generation',
  STORYBOARD_CREATION = 'storyboard_creation',
  VIDEO_GENERATION = 'video_generation',
  VOICE_SYNTHESIS = 'voice_synthesis',
  MUSIC_GENERATION = 'music_generation',
  POST_PROCESSING = 'post_processing',
  QUALITY_CHECK = 'quality_check',
  FINAL_RENDER = 'final_render'
}

export enum TaskStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

// API Request/Response Types
export interface GenerateVideoRequest {
  projectId: string
  text: string
  settings: VideoSettings
  voiceOver?: VoiceOverConfig
  music?: MusicConfig
}

export interface GenerateVideoResponse {
  projectId: string
  status: ProjectStatus
  estimatedTime: number
  queuePosition?: number
  tasks: PipelineTask[]
}

// Cost Estimation
export interface CostEstimate {
  engineCost: number
  voiceOverCost: number
  musicCost: number
  storageCost: number
  processingCost: number
  totalCost: number
  credits?: number
}

// Quality Control
export interface QualityCheckResult {
  passed: boolean
  issues: QualityIssue[]
  recommendations: string[]
  score: number
}

export interface QualityIssue {
  type: IssueType
  severity: IssueSeverity
  description: string
  timestamp?: number
  frame?: number
}

export enum IssueType {
  POLICY_VIOLATION = 'policy_violation',
  COPYRIGHT_CONCERN = 'copyright_concern',
  QUALITY_LOW = 'quality_low',
  AUDIO_SYNC = 'audio_sync',
  VISUAL_ARTIFACT = 'visual_artifact',
  DURATION_EXCEEDED = 'duration_exceeded'
}

export enum IssueSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}