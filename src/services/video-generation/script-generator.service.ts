import {
  VideoScript,
  ScriptBeat,
  EmotionKeyword,
  CameraMovement,
  VisualHook,
} from '@/types/video'
import { generateId } from '@/lib/utils'

interface ScriptGeneratorConfig {
  apiKey: string
  model?: string
  maxBeats?: number
  targetDuration?: number
}

export class ScriptGeneratorService {
  private config: ScriptGeneratorConfig

  constructor(config: ScriptGeneratorConfig) {
    this.config = {
      model: 'gpt-4-turbo',
      maxBeats: 10,
      targetDuration: 60,
      ...config,
    }
  }

  async generateScript(
    text: string,
    projectId: string,
    duration: number = 60
  ): Promise<VideoScript> {
    const beats = await this.generateBeats(text, duration)
    
    return {
      id: generateId(),
      projectId,
      rawText: text,
      beats,
      duration,
    }
  }

  private async generateBeats(text: string, targetDuration: number): Promise<ScriptBeat[]> {
    const prompt = this.buildScriptPrompt(text, targetDuration)
    
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: this.config.model,
        messages: [
          {
            role: 'system',
            content: `You are a Senior Screenwriter specializing in short-form video content. 
            Create compelling visual narratives that work well with AI video generation.`,
          },
          {
            role: 'user',
            content: prompt,
          },
        ],
        temperature: 0.7,
        response_format: { type: 'json_object' },
      }),
    })

    const data = await response.json()
    const scriptData = JSON.parse(data.choices[0].message.content)
    
    return this.parseBeats(scriptData.beats, targetDuration)
  }

  private buildScriptPrompt(text: string, duration: number): string {
    const beatsCount = Math.ceil(duration / 7) // ~7 seconds per beat
    
    return `
    Transform this concept into a ${duration}-second video script with ${beatsCount} beats.
    
    Input: "${text}"
    
    Break it into beats using a three-act structure. For each beat, provide:
    - beatNumber: sequential number
    - logline: concise description (max 20 words)
    - voText: voice-over text (max 25 words)
    - emotion: one of [excited, calm, dramatic, mysterious, happy, sad, tense, romantic]
    - visualHook: 
      - camera: one of [static, pan_left, pan_right, zoom_in, zoom_out, dolly_in, dolly_out, tracking, aerial]
      - subject: main visual element
      - style: visual style descriptor
      - lighting: lighting description
    - duration: seconds for this beat
    
    Return as JSON with structure: { beats: [...] }
    
    Ensure:
    - Total duration equals ${duration} seconds
    - Smooth narrative flow
    - Visual variety
    - Emotional arc
    `
  }

  private parseBeats(rawBeats: any[], targetDuration: number): ScriptBeat[] {
    const totalRawDuration = rawBeats.reduce((sum, beat) => sum + beat.duration, 0)
    const durationScale = targetDuration / totalRawDuration
    
    let timestamp = 0
    return rawBeats.map((beat, index) => {
      const scaledDuration = Math.round(beat.duration * durationScale)
      const scriptBeat: ScriptBeat = {
        id: generateId(),
        beatNumber: index + 1,
        logline: beat.logline,
        voText: beat.voText,
        emotion: this.mapEmotion(beat.emotion),
        visualHook: {
          camera: this.mapCameraMovement(beat.visualHook.camera),
          subject: beat.visualHook.subject,
          style: beat.visualHook.style,
          lighting: beat.visualHook.lighting,
        },
        duration: scaledDuration,
        timestamp,
      }
      timestamp += scaledDuration
      return scriptBeat
    })
  }

  private mapEmotion(emotion: string): EmotionKeyword {
    const emotionMap: Record<string, EmotionKeyword> = {
      excited: EmotionKeyword.EXCITED,
      calm: EmotionKeyword.CALM,
      dramatic: EmotionKeyword.DRAMATIC,
      mysterious: EmotionKeyword.MYSTERIOUS,
      happy: EmotionKeyword.HAPPY,
      sad: EmotionKeyword.SAD,
      tense: EmotionKeyword.TENSE,
      romantic: EmotionKeyword.ROMANTIC,
    }
    return emotionMap[emotion.toLowerCase()] || EmotionKeyword.CALM
  }

  private mapCameraMovement(camera: string): CameraMovement {
    const cameraMap: Record<string, CameraMovement> = {
      static: CameraMovement.STATIC,
      pan_left: CameraMovement.PAN_LEFT,
      pan_right: CameraMovement.PAN_RIGHT,
      zoom_in: CameraMovement.ZOOM_IN,
      zoom_out: CameraMovement.ZOOM_OUT,
      dolly_in: CameraMovement.DOLLY_IN,
      dolly_out: CameraMovement.DOLLY_OUT,
      tracking: CameraMovement.TRACKING,
      aerial: CameraMovement.AERIAL,
    }
    return cameraMap[camera.toLowerCase()] || CameraMovement.STATIC
  }

  async refineScript(script: VideoScript, feedback: string): Promise<VideoScript> {
    const prompt = `
    Refine this video script based on feedback:
    
    Current script: ${JSON.stringify(script.beats)}
    Feedback: ${feedback}
    
    Maintain the same structure but improve based on the feedback.
    Return as JSON with structure: { beats: [...] }
    `

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: this.config.model,
        messages: [
          {
            role: 'system',
            content: 'You are a Senior Screenwriter. Refine scripts based on feedback while maintaining structure.',
          },
          {
            role: 'user',
            content: prompt,
          },
        ],
        temperature: 0.7,
        response_format: { type: 'json_object' },
      }),
    })

    const data = await response.json()
    const refinedData = JSON.parse(data.choices[0].message.content)
    
    return {
      ...script,
      beats: this.parseBeats(refinedData.beats, script.duration),
    }
  }

  // Generate alternative versions for A/B testing
  async generateVariations(
    text: string,
    projectId: string,
    count: number = 3
  ): Promise<VideoScript[]> {
    const variations: VideoScript[] = []
    
    for (let i = 0; i < count; i++) {
      const script = await this.generateScript(
        text,
        projectId,
        this.config.targetDuration!
      )
      variations.push(script)
    }
    
    return variations
  }

  // Analyze script for potential issues
  analyzeScript(script: VideoScript): {
    issues: string[]
    suggestions: string[]
    score: number
  } {
    const issues: string[] = []
    const suggestions: string[] = []
    let score = 100

    // Check beat duration balance
    const avgDuration = script.duration / script.beats.length
    script.beats.forEach((beat, index) => {
      if (beat.duration > avgDuration * 2) {
        issues.push(`Beat ${index + 1} is too long (${beat.duration}s)`)
        score -= 5
      }
      if (beat.duration < avgDuration * 0.5) {
        issues.push(`Beat ${index + 1} is too short (${beat.duration}s)`)
        score -= 5
      }
    })

    // Check voice-over length
    script.beats.forEach((beat, index) => {
      const wordsPerSecond = beat.voText.split(' ').length / beat.duration
      if (wordsPerSecond > 3) {
        issues.push(`Beat ${index + 1} has too much voice-over text`)
        suggestions.push(`Reduce voice-over text for beat ${index + 1}`)
        score -= 3
      }
    })

    // Check visual variety
    const cameraMovements = script.beats.map(b => b.visualHook.camera)
    const uniqueMovements = new Set(cameraMovements).size
    if (uniqueMovements < script.beats.length * 0.5) {
      suggestions.push('Add more camera movement variety')
      score -= 10
    }

    // Check emotional arc
    const emotions = script.beats.map(b => b.emotion)
    const uniqueEmotions = new Set(emotions).size
    if (uniqueEmotions < 3) {
      suggestions.push('Consider adding more emotional variety')
      score -= 5
    }

    return { issues, suggestions, score: Math.max(0, score) }
  }
}