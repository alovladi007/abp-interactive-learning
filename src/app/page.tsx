import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  ArrowRight,
  PlayCircle,
  Sparkles,
  BookOpen,
  Users,
  Award,
  TrendingUp,
  Shield,
  Zap,
  Globe,
  BarChart3,
  Brain,
  Rocket,
  Star,
  CheckCircle,
  Video,
  GraduationCap,
  Building2,
  DollarSign,
} from "lucide-react"

const features = [
  {
    title: "AI-Powered Video Generation",
    description: "Transform any text or document into engaging video content with our advanced AI technology.",
    icon: Brain,
    gradient: "from-purple-500 to-pink-500",
  },
  {
    title: "Interactive Learning Paths",
    description: "Personalized learning journeys that adapt to your pace and learning style.",
    icon: Rocket,
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    title: "Professional Certifications",
    description: "Earn recognized certifications from top institutions and industry leaders.",
    icon: Award,
    gradient: "from-orange-500 to-red-500",
  },
  {
    title: "Live Collaboration",
    description: "Learn together with real-time chat, screen sharing, and collaborative tools.",
    icon: Users,
    gradient: "from-green-500 to-emerald-500",
  },
  {
    title: "Advanced Analytics",
    description: "Track your progress with detailed insights and performance metrics.",
    icon: BarChart3,
    gradient: "from-indigo-500 to-purple-500",
  },
  {
    title: "Global Marketplace",
    description: "Buy and sell courses, create your own content, and monetize your expertise.",
    icon: Globe,
    gradient: "from-yellow-500 to-orange-500",
  },
]

const stats = [
  { label: "Active Learners", value: "10M+", icon: Users },
  { label: "Video Courses", value: "500K+", icon: Video },
  { label: "Certifications", value: "1000+", icon: Award },
  { label: "Countries", value: "195", icon: Globe },
]

const testimonials = [
  {
    name: "Sarah Johnson",
    role: "Software Engineer at Google",
    content: "ABP Learning transformed my career. The AI-generated videos made complex topics easy to understand.",
    rating: 5,
  },
  {
    name: "Michael Chen",
    role: "Data Scientist",
    content: "The certification programs are top-notch. I landed my dream job after completing the ML pathway.",
    rating: 5,
  },
  {
    name: "Emily Rodriguez",
    role: "Product Manager",
    content: "The interactive features and community support make learning enjoyable and effective.",
    rating: 5,
  },
]

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/10 via-background to-background">
        <div className="absolute inset-0 bg-grid-white/10 bg-[size:20px_20px] [mask-image:radial-gradient(white,transparent_70%)]" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="text-center">
            <Badge variant="outline" className="mb-4 animate-fade-in">
              <Sparkles className="mr-1 h-3 w-3" />
              AI-Powered Learning Platform
            </Badge>
            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl animate-slide-up">
              Learn Anything,
              <span className="block gradient-primary text-gradient">
                Master Everything
              </span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground animate-slide-up animation-delay-100">
              Experience the future of education with AI-generated videos, interactive courses,
              professional certifications, and a global learning community.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up animation-delay-200">
              <Button size="xl" variant="gradient" className="group">
                Start Learning Free
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
              <Button size="xl" variant="outline" className="group">
                <PlayCircle className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </div>
          </div>

          {/* Hero Image/Video Preview */}
          <div className="mt-16 relative">
            <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent z-10" />
            <div className="relative rounded-xl overflow-hidden shadow-2xl border bg-card">
              <div className="aspect-video bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
                <PlayCircle className="h-24 w-24 text-primary/50" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-muted/50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <stat.icon className="mx-auto h-8 w-8 text-primary mb-2" />
                <div className="text-3xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">
              Everything You Need to Succeed
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Powerful features that make learning effective and enjoyable
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.title} className="group hover:shadow-lg transition-all hover:-translate-y-1">
                <CardHeader>
                  <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${feature.gradient} text-white mb-4`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Video Showcase Section */}
      <section className="py-24 bg-muted/50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold sm:text-4xl">Popular Courses</h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Explore our most popular video courses and start learning today
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i} className="overflow-hidden hover:shadow-lg transition-all hover:-translate-y-1">
                <div className="aspect-video bg-gradient-to-br from-primary/20 to-secondary/20 relative">
                  <Badge className="absolute top-2 left-2">Bestseller</Badge>
                  <PlayCircle className="absolute inset-0 m-auto h-12 w-12 text-white/80" />
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold mb-1">Advanced Machine Learning</h3>
                  <p className="text-sm text-muted-foreground mb-2">Dr. Sarah Williams</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Star className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                      <span className="ml-1 text-sm">4.9 (2.3k)</span>
                    </div>
                    <span className="font-semibold">$49.99</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="text-center mt-8">
            <Button variant="outline" size="lg">
              Browse All Courses
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold sm:text-4xl">What Learners Say</h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Join millions of satisfied learners worldwide
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-3">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.name}>
                <CardContent className="p-6">
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 fill-yellow-500 text-yellow-500" />
                    ))}
                  </div>
                  <p className="text-muted-foreground mb-4">"{testimonial.content}"</p>
                  <div>
                    <p className="font-semibold">{testimonial.name}</p>
                    <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-primary text-primary-foreground">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold sm:text-4xl mb-4">
            Ready to Transform Your Learning?
          </h2>
          <p className="text-lg mb-8 opacity-90 max-w-2xl mx-auto">
            Join millions of learners and start your journey today with our free tier.
            No credit card required.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="xl" variant="secondary" className="group">
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>
            <Button size="xl" variant="outline" className="bg-transparent text-primary-foreground border-primary-foreground hover:bg-primary-foreground hover:text-primary">
              View Pricing
            </Button>
          </div>
          <div className="mt-8 flex items-center justify-center gap-8 text-sm">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              No credit card required
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              Free forever plan
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              Cancel anytime
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
