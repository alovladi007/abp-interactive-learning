'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Resource {
  resource_id: string
  title: string
  provider: string
  type: string
  time_est_hours: number
  quality_score: number
  cost: string
}

interface RoadmapStep {
  skill_id: string
  skill_name: string
  resources: Resource[]
  est_hours: number
  start_week: number
  end_week: number
}

interface Roadmap {
  sequence: RoadmapStep[]
  milestones: any[]
  summary: any
  estimated_completion: string
}

export default function Home() {
  const [formData, setFormData] = useState({
    major: 'cs',
    goal: 'ml-engineer',
    weekly_hours: 15,
    horizon_months: 12,
    budget: 200,
    baseline: '',
    learning_style: 'mixed'
  })
  
  const [loading, setLoading] = useState(false)
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState('form')

  const generateRoadmap = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post(`${API_URL}/plan`, {
        major: formData.major,
        goal: formData.goal,
        horizon_months: formData.horizon_months,
        weekly_hours: formData.weekly_hours,
        budget: formData.budget,
        baseline_mastered: formData.baseline.split(',').map(s => s.trim()).filter(Boolean),
        learning_style: formData.learning_style
      })
      
      setRoadmap(response.data)
      setActiveTab('roadmap')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            AI Path Advisor
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Generate personalized learning roadmaps for your career goals
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('form')}
                className={`py-4 px-6 text-sm font-medium ${
                  activeTab === 'form'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Setup
              </button>
              <button
                onClick={() => setActiveTab('roadmap')}
                disabled={!roadmap}
                className={`py-4 px-6 text-sm font-medium ${
                  activeTab === 'roadmap'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                } ${!roadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                Roadmap
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'form' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Major/Field
                  </label>
                  <select
                    value={formData.major}
                    onChange={(e) => setFormData({...formData, major: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="cs">Computer Science</option>
                    <option value="ee">Electrical Engineering</option>
                    <option value="physics">Physics</option>
                    <option value="data-science">Data Science</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Career Goal
                  </label>
                  <select
                    value={formData.goal}
                    onChange={(e) => setFormData({...formData, goal: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="ml-engineer">Machine Learning Engineer</option>
                    <option value="data-engineer">Data Engineer</option>
                    <option value="embedded-engineer">Embedded Systems Engineer</option>
                    <option value="full-stack">Full Stack Developer</option>
                    <option value="security-engineer">Security Engineer</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Weekly Study Hours: {formData.weekly_hours}
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="40"
                    value={formData.weekly_hours}
                    onChange={(e) => setFormData({...formData, weekly_hours: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Time Horizon (months): {formData.horizon_months}
                  </label>
                  <input
                    type="range"
                    min="3"
                    max="36"
                    value={formData.horizon_months}
                    onChange={(e) => setFormData({...formData, horizon_months: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Monthly Budget ($): {formData.budget}
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="500"
                    step="50"
                    value={formData.budget}
                    onChange={(e) => setFormData({...formData, budget: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Learning Style
                  </label>
                  <select
                    value={formData.learning_style}
                    onChange={(e) => setFormData({...formData, learning_style: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="visual">Visual (Videos)</option>
                    <option value="reading">Reading (Books)</option>
                    <option value="hands-on">Hands-on (Projects)</option>
                    <option value="mixed">Mixed</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Already Mastered Skills (comma-separated skill IDs)
                  </label>
                  <textarea
                    value={formData.baseline}
                    onChange={(e) => setFormData({...formData, baseline: e.target.value})}
                    placeholder="e.g., prog.python.basics, math.calculus_1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>

                <div className="md:col-span-2">
                  <button
                    onClick={generateRoadmap}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                  >
                    {loading ? 'Generating...' : 'Generate Roadmap'}
                  </button>
                  
                  {error && (
                    <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                      {error}
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'roadmap' && roadmap && (
              <div>
                <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                  <h2 className="text-xl font-bold mb-2">Your Learning Path</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Skills</p>
                      <p className="text-2xl font-bold">{roadmap.summary.total_skills}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Duration</p>
                      <p className="text-2xl font-bold">{roadmap.summary.completion_months} months</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Hours</p>
                      <p className="text-2xl font-bold">{roadmap.summary.total_hours}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Completion</p>
                      <p className="text-2xl font-bold">{roadmap.estimated_completion}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold mb-4">Learning Sequence</h3>
                  {roadmap.sequence.map((step, index) => (
                    <div key={step.skill_id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-semibold text-lg">
                            {index + 1}. {step.skill_name}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Weeks {step.start_week}-{step.end_week} • {step.est_hours} hours
                          </p>
                        </div>
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          Week {step.start_week}
                        </span>
                      </div>
                      
                      <div className="mt-3">
                        <p className="text-sm font-medium mb-2">Resources:</p>
                        <div className="space-y-2">
                          {step.resources.map((resource) => (
                            <div key={resource.resource_id} className="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-900 rounded">
                              <div>
                                <p className="font-medium text-sm">{resource.title}</p>
                                <p className="text-xs text-gray-600 dark:text-gray-400">
                                  {resource.provider} • {resource.type} • {resource.time_est_hours}h
                                </p>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-1 rounded text-xs ${
                                  resource.cost === 'free' 
                                    ? 'bg-green-100 text-green-800' 
                                    : 'bg-yellow-100 text-yellow-800'
                                }`}>
                                  {resource.cost}
                                </span>
                                <span className="text-xs font-semibold">
                                  {resource.quality_score}/10
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-8">
                  <h3 className="text-lg font-semibold mb-4">Milestones</h3>
                  <div className="space-y-2">
                    {roadmap.milestones.map((milestone, index) => (
                      <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 dark:bg-gray-900 rounded">
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="font-bold text-blue-600">W{milestone.week}</span>
                        </div>
                        <div>
                          <p className="font-medium">{milestone.name}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{milestone.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
