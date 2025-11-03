'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { 
  Brain, 
  Zap, 
  Shield, 
  Copy, 
  Wand2, 
  Sparkles,
  FileText,
  Settings,
  CheckCircle,
  Loader2,
  Moon,
  Sun
} from 'lucide-react'

export default function Home() {
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [tone, setTone] = useState('casual')
  const [copied, setCopied] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(true)
  const [progress, setProgress] = useState(0)

  const handleHumanize = async () => {
    if (!inputText.trim()) return
    
    setIsLoading(true)
    setProgress(0)
    
    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + Math.random() * 15
      })
    }, 200)
    
    try {
      const response = await fetch('/api/humanize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          tone: tone,
        }),
      })
      
      const data = await response.json()
      setProgress(100)
      setOutputText(data.humanizedText)
    } catch (error) {
      console.error('Error:', error)
      setOutputText('Error occurred while processing text. Please try again.')
    } finally {
      clearInterval(progressInterval)
      setTimeout(() => {
        setIsLoading(false)
        setProgress(0)
      }, 500)
    }
  }

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(outputText)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const getToneIcon = (tone: string) => {
    switch (tone) {
      case 'casual': return '😊'
      case 'formal': return '👔'
      case 'creative': return '🎨'
      case 'academic': return '🎓'
      default: return '📝'
    }
  }

  const getToneDescription = (tone: string) => {
    switch (tone) {
      case 'casual': return 'Friendly and conversational'
      case 'formal': return 'Professional and structured'
      case 'creative': return 'Engaging and compelling'
      case 'academic': return 'Scholarly and precise'
      default: return 'Neutral tone'
    }
  }

  return (
    <div className="min-h-screen particle-bg bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 animate-gradient">
      {/* Header */}
      <div className="relative border-b glass-morphism-dark">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20 animate-gradient"></div>
        <div className="relative container mx-auto px-4 py-12">
          {/* Dark Mode Toggle */}
          <div className="absolute top-4 right-4">
            <Button
              onClick={() => setIsDarkMode(!isDarkMode)}
              variant="ghost"
              size="sm"
              className="glass-morphism border-white/20 text-white hover:bg-white/10 magnetic-hover"
            >
              {isDarkMode ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
          </div>
          <div className="text-center space-y-6">
            <div className="flex items-center justify-center gap-4 slide-in-up">
              <div className="p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl floating pulse-glow magnetic-hover">
                <Brain className="h-12 w-12 text-white" />
              </div>
              <h1 className="text-6xl font-bold font-primary text-shimmer typing-animation">
                AI Text Humanizer
              </h1>
            </div>
            <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed font-body fade-in-scale" style={{animationDelay: '0.5s'}}>
              Transform AI-generated text into natural, human-like content with advanced paraphrasing technology
            </p>
            <div className="flex justify-center gap-4 flex-wrap fade-in-scale" style={{animationDelay: '1s'}}>
              <Badge variant="secondary" className="gap-2 glass-morphism text-white border-white/20 px-4 py-2 magnetic-hover glow-on-hover">
                <Shield className="h-4 w-4" />
                Privacy First
              </Badge>
              <Badge variant="secondary" className="gap-2 glass-morphism text-white border-white/20 px-4 py-2 magnetic-hover glow-on-hover">
                <Zap className="h-4 w-4" />
                Instant Results
              </Badge>
              <Badge variant="secondary" className="gap-2 glass-morphism text-white border-white/20 px-4 py-2 magnetic-hover glow-on-hover">
                <Sparkles className="h-4 w-4" />
                Multiple Tones
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Input Section */}
          <Card className="h-fit glass-morphism-dark border-white/20 card-hover slide-in-up" style={{animationDelay: '1.5s'}}>
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-white font-secondary font-semibold">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg magnetic-hover">
                  <FileText className="h-5 w-5 text-white" />
                </div>
                Original Text
              </CardTitle>
              <CardDescription className="text-white/70 font-body">
                Paste your AI-generated content here
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Tone Selector */}
              <div className="space-y-3">
                <label className="text-sm font-medium flex items-center gap-2 text-white">
                  <Settings className="h-4 w-4" />
                  Writing Tone
                </label>
                <Select value={tone} onValueChange={setTone}>
                  <SelectTrigger className="w-full glass-morphism border-white/20 text-white">
                    <SelectValue placeholder="Select a tone" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="casual">
                      <div className="flex items-center gap-2">
                        <span>{getToneIcon('casual')}</span>
                        <div>
                          <div className="font-medium">Casual & Friendly</div>
                          <div className="text-xs text-muted-foreground">Friendly and conversational</div>
                        </div>
                      </div>
                    </SelectItem>
                    <SelectItem value="formal">
                      <div className="flex items-center gap-2">
                        <span>{getToneIcon('formal')}</span>
                        <div>
                          <div className="font-medium">Formal & Professional</div>
                          <div className="text-xs text-muted-foreground">Professional and structured</div>
                        </div>
                      </div>
                    </SelectItem>
                    <SelectItem value="creative">
                      <div className="flex items-center gap-2">
                        <span>{getToneIcon('creative')}</span>
                        <div>
                          <div className="font-medium">Creative & Engaging</div>
                          <div className="text-xs text-muted-foreground">Engaging and compelling</div>
                        </div>
                      </div>
                    </SelectItem>
                    <SelectItem value="academic">
                      <div className="flex items-center gap-2">
                        <span>{getToneIcon('academic')}</span>
                        <div>
                          <div className="font-medium">Academic & Scholarly</div>
                          <div className="text-xs text-muted-foreground">Scholarly and precise</div>
                        </div>
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Paste your AI-generated text here to make it sound more human..."
                className="min-h-[200px] resize-none glass-morphism border-white/20 text-white placeholder:text-white/50 bg-transparent"
              />

              <div className="flex items-center justify-between">
                <Badge variant="outline" className="gap-1 glass-morphism border-white/20 text-white">
                  {inputText.length} characters
                </Badge>
                <Button 
                  onClick={handleHumanize}
                  disabled={!inputText.trim() || isLoading}
                  className="gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 button-glow pulse-glow"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span className="loading-dots">Humanizing</span>
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-4 w-4" />
                      Humanize Text
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Output Section */}
          <Card className="h-fit glass-morphism-dark border-white/20 card-hover slide-in-up" style={{animationDelay: '2s'}}>
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-white font-secondary font-semibold">
                <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg magnetic-hover">
                  <CheckCircle className="h-5 w-5 text-white" />
                </div>
                Humanized Text
              </CardTitle>
              <CardDescription className="text-white/70 font-body">
                Your natural, human-like content
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Progress Bar */}
              {isLoading && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm text-white/70">
                    <span>Processing...</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all duration-300 ease-out"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              )}
              
              <div className="relative">
                <Textarea
                  value={outputText}
                  readOnly
                  placeholder="Your humanized text will appear here..."
                  className="min-h-[200px] resize-none glass-morphism border-white/20 text-white placeholder:text-white/50 bg-transparent"
                />
                {outputText && (
                  <Button
                    onClick={copyToClipboard}
                    size="sm"
                    variant="secondary"
                    className="absolute top-3 right-3 gap-2 glass-morphism border-white/20 text-white hover:bg-white/10 button-glow"
                  >
                    {copied ? (
                      <>
                        <CheckCircle className="h-3 w-3" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="h-3 w-3" />
                        Copy
                      </>
                    )}
                  </Button>
                )}
              </div>
              
              {outputText && (
                <div className="flex items-center justify-between text-sm">
                  <Badge variant="outline" className="gap-1 glass-morphism border-white/20 text-white">
                    {outputText.length} characters
                  </Badge>
                  <Badge variant="secondary" className="gap-1 glass-morphism border-white/20 text-white">
                    {getToneIcon(tone)} {getToneDescription(tone)}
                  </Badge>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Features Section */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 text-white font-primary">Why Choose Our Humanizer?</h2>
            <p className="text-white/70 text-lg font-body">Advanced features to make your content undetectable</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="text-center glass-morphism-dark border-white/20 card-hover group">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-6 floating">
                  <Shield className="h-8 w-8 text-white" />
                </div>
                <CardTitle className="text-white text-xl font-secondary font-semibold">AI Detection Bypass</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-white/70 text-base leading-relaxed font-body">
                  Advanced algorithms to make your text undetectable by AI content detectors
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center glass-morphism-dark border-white/20 card-hover group">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mb-6 floating" style={{animationDelay: '1s'}}>
                  <Sparkles className="h-8 w-8 text-white" />
                </div>
                <CardTitle className="text-white text-xl font-secondary font-semibold">Multiple Tones</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-white/70 text-base leading-relaxed font-body">
                  Choose from various writing styles to match your specific needs and audience
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center glass-morphism-dark border-white/20 card-hover group">
              <CardHeader>
                <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-6 floating" style={{animationDelay: '2s'}}>
                  <Brain className="h-8 w-8 text-white" />
                </div>
                <CardTitle className="text-white text-xl font-secondary font-semibold">Smart Processing</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-white/70 text-base leading-relaxed font-body">
                  Intelligent text analysis and natural language processing for better results
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
