import {
  Storyboard,
  StoryboardFrame,
  VideoScript,
  ScriptBeat,
  FrameMetadata,
  AspectRatio,
  Resolution,
  VideoStyle,
  StylePreset,
} from '@/types/video'
import { generateId } from '@/lib/utils'

interface StoryboardConfig {
  apiKey: string
  imageModel?: string
  defaultStyle?: StylePreset
  defaultResolution?: Resolution
  defaultAspectRatio?: AspectRatio
}

export class StoryboardGeneratorService {
  private config: StoryboardConfig

  constructor(config: StoryboardConfig) {
    this.config = {
      imageModel: 'dall-e-3',
      defaultStyle: StylePreset.CINEMATIC,
      defaultResolution: Resolution.FHD,
      defaultAspectRatio: AspectRatio.SIXTEEN_NINE,
      ...config,
    }
  }

  async generateStoryboard(
    script: VideoScript,
    style: VideoStyle,
    aspectRatio: AspectRatio = AspectRatio.SIXTEEN_NINE,
    resolution: Resolution = Resolution.FHD
  ): Promise<Storyboard> {
    const frames = await Promise.all(
      script.beats.map((beat) =>
        this.generateFrame(beat, style, aspectRatio, resolution, script.projectId)
      )
    )

    return {
      id: generateId(),
      projectId: script.projectId,
      frames,
    }
  }

  private async generateFrame(
    beat: ScriptBeat,
    style: VideoStyle,
    aspectRatio: AspectRatio,
    resolution: Resolution,
    projectId: string
  ): Promise<StoryboardFrame> {
    const prompt = this.buildVisualPrompt(beat, style)
    const negativePrompt = this.buildNegativePrompt(style)
    const seed = `SB_${projectId}_${beat.beatNumber}`

    // Generate storyboard image
    const imageUrl = await this.generateImage(prompt, aspectRatio)

    return {
      id: generateId(),
      beatId: beat.id,
      prompt,
      negativePrompt,
      seed,
      imageUrl,
      thumbnailUrl: imageUrl, // In production, generate a smaller thumbnail
      metadata: {
        style: style.name,
        lighting: beat.visualHook.lighting || 'natural lighting',
        colorGrade: this.getColorGrade(style, beat.emotion),
        aspectRatio,
        resolution,
      },
    }
  }

  private buildVisualPrompt(beat: ScriptBeat, style: VideoStyle): string {
    const { visualHook, emotion } = beat
    const stylePrompt = this.getStylePrompt(style)
    const emotionModifier = this.getEmotionModifier(emotion)
    const cameraDescription = this.getCameraDescription(visualHook.camera)

    // Build comprehensive prompt
    const elements = [
      visualHook.subject,
      cameraDescription,
      visualHook.style,
      visualHook.lighting,
      stylePrompt,
      emotionModifier,
      'high quality',
      'detailed',
      'professional cinematography',
    ].filter(Boolean)

    return elements.join(', ')
  }

  private buildNegativePrompt(style: VideoStyle): string {
    const baseNegative = [
      'low quality',
      'blurry',
      'distorted',
      'watermark',
      'text',
      'logo',
      'signature',
      'artifacts',
      'noise',
      'grain',
    ]

    // Add style-specific negatives
    switch (style.preset) {
      case StylePreset.PHOTOREALISTIC:
        baseNegative.push('cartoon', 'anime', 'illustration', 'painting')
        break
      case StylePreset.ANIME:
        baseNegative.push('realistic', 'photo', '3d render')
        break
      case StylePreset.CINEMATIC:
        baseNegative.push('amateur', 'handheld', 'shaky')
        break
    }

    return baseNegative.join(', ')
  }

  private async generateImage(prompt: string, aspectRatio: AspectRatio): Promise<string> {
    const size = this.mapAspectRatioToSize(aspectRatio)

    const response = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: this.config.imageModel,
        prompt,
        n: 1,
        size,
        quality: 'hd',
        style: 'vivid',
      }),
    })

    const data = await response.json()
    return data.data[0].url
  }

  private getStylePrompt(style: VideoStyle): string {
    if (style.customPrompt) {
      return style.customPrompt
    }

    const stylePrompts: Record<StylePreset, string> = {
      [StylePreset.CINEMATIC]: 'cinematic style, film grain, anamorphic lens, depth of field',
      [StylePreset.ANIME]: 'anime style, cel shaded, vibrant colors, Studio Ghibli inspired',
      [StylePreset.PHOTOREALISTIC]: 'photorealistic, hyperrealistic, 8k photography, natural lighting',
      [StylePreset.CARTOON]: '3D cartoon style, Pixar quality, colorful, friendly',
      [StylePreset.WATERCOLOR]: 'watercolor painting, soft edges, artistic, traditional media',
      [StylePreset.OIL_PAINTING]: 'oil painting, impressionist, thick brushstrokes, artistic',
      [StylePreset.SKETCH]: 'pencil sketch, line art, black and white, detailed drawing',
      [StylePreset.CYBERPUNK]: 'cyberpunk aesthetic, neon lights, futuristic, high tech',
      [StylePreset.FANTASY]: 'fantasy art, magical, ethereal, epic landscape',
    }

    return stylePrompts[style.preset!] || ''
  }

  private getEmotionModifier(emotion: string): string {
    const emotionModifiers: Record<string, string> = {
      excited: 'dynamic, energetic, vibrant',
      calm: 'serene, peaceful, tranquil',
      dramatic: 'intense, high contrast, moody',
      mysterious: 'enigmatic, shadowy, atmospheric',
      happy: 'bright, cheerful, warm colors',
      sad: 'melancholic, muted colors, somber',
      tense: 'suspenseful, dark shadows, sharp contrasts',
      romantic: 'soft lighting, warm tones, dreamy',
    }

    return emotionModifiers[emotion] || ''
  }

  private getCameraDescription(camera: string): string {
    const cameraDescriptions: Record<string, string> = {
      static: 'static shot',
      pan_left: 'camera panning left',
      pan_right: 'camera panning right',
      zoom_in: 'zooming in',
      zoom_out: 'zooming out',
      dolly_in: 'dolly shot moving forward',
      dolly_out: 'dolly shot moving backward',
      tracking: 'tracking shot',
      aerial: 'aerial view, drone shot',
    }

    return cameraDescriptions[camera] || 'medium shot'
  }

  private getColorGrade(style: VideoStyle, emotion: string): string {
    // Style-based color grading
    const styleGrades: Partial<Record<StylePreset, string>> = {
      [StylePreset.CINEMATIC]: 'teal and orange',
      [StylePreset.CYBERPUNK]: 'neon pink and blue',
      [StylePreset.FANTASY]: 'ethereal glow',
      [StylePreset.ANIME]: 'vibrant saturation',
    }

    // Emotion-based overrides
    const emotionGrades: Record<string, string> = {
      dramatic: 'high contrast, desaturated',
      happy: 'warm, golden hour',
      sad: 'cool, desaturated blues',
      mysterious: 'deep shadows, muted tones',
      romantic: 'soft, warm pink tones',
    }

    return emotionGrades[emotion] || styleGrades[style.preset!] || 'natural colors'
  }

  private mapAspectRatioToSize(aspectRatio: AspectRatio): string {
    // DALL-E 3 supported sizes
    const sizeMap: Record<AspectRatio, string> = {
      [AspectRatio.SIXTEEN_NINE]: '1792x1024', // Wide
      [AspectRatio.NINE_SIXTEEN]: '1024x1792', // Tall
      [AspectRatio.ONE_ONE]: '1024x1024', // Square
      [AspectRatio.FOUR_THREE]: '1024x1024', // Use square as fallback
      [AspectRatio.TWENTY_ONE_NINE]: '1792x1024', // Use wide as fallback
    }

    return sizeMap[aspectRatio] || '1024x1024'
  }

  // Generate multiple style variations for A/B testing
  async generateStyleVariations(
    script: VideoScript,
    styles: VideoStyle[],
    aspectRatio: AspectRatio,
    resolution: Resolution
  ): Promise<Storyboard[]> {
    return Promise.all(
      styles.map((style) =>
        this.generateStoryboard(script, style, aspectRatio, resolution)
      )
    )
  }

  // Update individual frame
  async regenerateFrame(
    beat: ScriptBeat,
    style: VideoStyle,
    aspectRatio: AspectRatio,
    resolution: Resolution,
    customPrompt?: string
  ): Promise<StoryboardFrame> {
    const baseFrame = await this.generateFrame(
      beat,
      style,
      aspectRatio,
      resolution,
      'temp'
    )

    if (customPrompt) {
      baseFrame.prompt = customPrompt
      baseFrame.imageUrl = await this.generateImage(customPrompt, aspectRatio)
    }

    return baseFrame
  }

  // Batch process multiple scripts
  async batchGenerateStoryboards(
    scripts: VideoScript[],
    style: VideoStyle,
    aspectRatio: AspectRatio,
    resolution: Resolution
  ): Promise<Storyboard[]> {
    // Process in batches to avoid rate limits
    const batchSize = 5
    const results: Storyboard[] = []

    for (let i = 0; i < scripts.length; i += batchSize) {
      const batch = scripts.slice(i, i + batchSize)
      const batchResults = await Promise.all(
        batch.map((script) =>
          this.generateStoryboard(script, style, aspectRatio, resolution)
        )
      )
      results.push(...batchResults)
      
      // Add delay to respect rate limits
      if (i + batchSize < scripts.length) {
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
    }

    return results
  }
}