import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import {
  Video,
  GraduationCap,
  Library,
  FileQuestion,
  Award,
  Users,
  PlayCircle,
  ArrowRight,
} from "lucide-react"

const features = [
  {
    icon: Video,
    title: "AI Video Generation",
    description: "Transform any text into engaging interactive video lectures with advanced AI technology.",
  },
  {
    icon: GraduationCap,
    title: "Academic Integration",
    description: "Seamlessly integrate with your academic curriculum and syllabus for personalized learning.",
  },
  {
    icon: Library,
    title: "Personal Library",
    description: "Build your own digital library with books, research papers, and learning materials.",
  },
  {
    icon: FileQuestion,
    title: "Interactive Quizzes",
    description: "Test your knowledge with AI-generated quizzes and assessments tailored to your content.",
  },
  {
    icon: Award,
    title: "Certifications",
    description: "Prepare for professional certifications with comprehensive study materials and practice exams.",
  },
  {
    icon: Users,
    title: "Corporate Training",
    description: "Enterprise solutions for employee training and skill development programs.",
  },
]

const samples = [
  {
    title: "Quantum Mechanics",
    description: "Explore the fundamentals of quantum physics through interactive visualizations.",
    image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop",
  },
  {
    title: "Semiconductor Physics",
    description: "Understand semiconductor devices and their applications in modern technology.",
    image: "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=300&h=200&fit=crop",
  },
  {
    title: "Machine Learning",
    description: "Learn ML algorithms and their practical implementations through visual examples.",
    image: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300&h=200&fit=crop",
  },
  {
    title: "Advanced Mathematics",
    description: "Master complex mathematical concepts with step-by-step visual explanations.",
    image: "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=200&fit=crop",
  },
]

const pricingPlans = [
  {
    name: "Free",
    price: "$0",
    period: "/month",
    features: [
      "Basic topics only",
      "3 videos per month",
      "Standard processing",
      "Community support",
    ],
    notIncluded: ["Advanced topics", "Priority support"],
  },
  {
    name: "Pro",
    price: "$19",
    period: "/month",
    featured: true,
    features: [
      "Unlimited videos",
      "Advanced topic support",
      "Faster processing",
      "Priority email support",
      "Quiz generation",
      "Personal library",
    ],
  },
  {
    name: "ProMax",
    price: "$49",
    period: "/month",
    features: [
      "Everything in Pro",
      "Corporate features",
      "API access",
      "White-label options",
      "Dedicated support",
      "Custom integrations",
    ],
  },
]

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-purple-50 via-white to-white dark:from-purple-950/20 dark:via-background dark:to-background">
        <div className="absolute inset-0 bg-grid-slate-100 [mask-image:radial-gradient(ellipse_at_center,white,transparent_70%)] dark:bg-grid-slate-800/25" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
                Transform Your Learning Experience
              </h1>
              <p className="mt-6 text-lg text-muted-foreground">
                Upload any text or chapter and watch it come to life through AI-powered interactive video lectures. 
                Perfect for students, professionals, and lifelong learners.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row gap-4">
                <Button size="lg" className="gradient-primary text-white" asChild>
                  <Link href="/dashboard">
                    Get Started Free
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link href="#samples">View Samples</Link>
                </Button>
              </div>
            </div>
            <div className="relative">
              <div className="grid grid-cols-2 gap-4">
                <img
                  src="https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop"
                  alt="Microchip Technology"
                  className="rounded-lg shadow-lg"
                />
                <img
                  src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=300&fit=crop"
                  alt="Data Visualization"
                  className="rounded-lg shadow-lg mt-8"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50 dark:bg-muted/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold sm:text-4xl">Powerful Learning Features</h2>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.title} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="h-12 w-12 rounded-lg gradient-primary flex items-center justify-center text-white mb-4">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Learning Samples */}
      <section id="samples" className="py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold sm:text-4xl">Interactive Learning Samples</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {samples.map((sample) => (
              <Card key={sample.title} className="overflow-hidden hover:shadow-lg transition-shadow">
                <div className="aspect-video relative">
                  <img
                    src={sample.image}
                    alt={sample.title}
                    className="object-cover w-full h-full"
                  />
                  <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                    <PlayCircle className="h-12 w-12 text-white" />
                  </div>
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold mb-1">{sample.title}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{sample.description}</p>
                  <Button variant="outline" size="sm" className="w-full">
                    Watch Sample
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-24 bg-gray-50 dark:bg-muted/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold sm:text-4xl">Choose Your Learning Plan</h2>
          </div>
          <div className="grid gap-8 lg:grid-cols-3">
            {pricingPlans.map((plan) => (
              <Card
                key={plan.name}
                className={`relative ${
                  plan.featured
                    ? "border-primary shadow-lg scale-105"
                    : ""
                }`}
              >
                {plan.featured && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                    <span className="bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm font-medium">
                      Most Popular
                    </span>
                  </div>
                )}
                <CardContent className="p-6">
                  <div className="text-center mb-6">
                    <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                    <div className="flex items-baseline justify-center">
                      <span className="text-4xl font-bold">{plan.price}</span>
                      <span className="text-muted-foreground ml-1">{plan.period}</span>
                    </div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-start">
                        <svg
                          className="h-5 w-5 text-green-500 mr-2 flex-shrink-0"
                          fill="none"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                    {plan.notIncluded?.map((feature) => (
                      <li key={feature} className="flex items-start opacity-50">
                        <svg
                          className="h-5 w-5 text-red-500 mr-2 flex-shrink-0"
                          fill="none"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button
                    className={`w-full ${
                      plan.featured ? "gradient-primary text-white" : ""
                    }`}
                    variant={plan.featured ? "default" : "outline"}
                  >
                    {plan.name === "Free" ? "Get Started" : `Choose ${plan.name}`}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
