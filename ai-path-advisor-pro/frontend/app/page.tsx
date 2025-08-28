'use client'
import { useEffect, useState } from 'react'

export default function Page() {
  const [mode, setMode] = useState<'major'|'role'>('role')
  const [role, setRole] = useState('software_engineer')
  const [roles, setRoles] = useState<{key:string, name:string}[]>([])
  const [major, setMajor] = useState('cs')
  const [weekly, setWeekly] = useState(12)
  const [months, setMonths] = useState(10)
  const [budget, setBudget] = useState(150)
  const [baseline, setBaseline] = useState('')
  const [preferFormats, setPreferFormats] = useState<string[]>(['video','labs'])
  const [wTime, setWTime] = useState(1.0)
  const [wCost, setWCost] = useState(0.5)
  const [wQuality, setWQuality] = useState(1.0)
  const [wDifficulty, setWDifficulty] = useState(0.1)
  const [variant, setVariant] = useState<'balanced'|'fastest'|'cheapest'|''>('balanced')
  const [loading, setLoading] = useState(false)
  const [plan, setPlan] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'config'|'quiz'|'roadmap'|'progress'>('config')

  // Quiz state
  const [quizItems, setQuizItems] = useState<any[]|null>(null)
  const [quizAnswers, setQuizAnswers] = useState<{[k:number]:number}>({})
  const [quizResult, setQuizResult] = useState<any|null>(null)

  // Progress / burndown
  const [actualByWeek, setActualByWeek] = useState<number[]>([])
  const [currentWeek, setCurrentWeek] = useState<number>(1)

  // Comparison state
  const [comparePlans, setComparePlans] = useState<any[]>([])

  useEffect(()=>{
    fetch('http://127.0.0.1:8000/roles')
      .then(r=>r.json())
      .then(data=>{
        setRoles(data.map((r:any)=>({key:r.key, name:r.name})))
      })
      .catch(err => console.error('Failed to load roles:', err))
  }, [])

  function computePlannedByWeek(plan:any): number[] {
    if (!plan) return []
    const weeks = plan.summary.weeks_total || 0
    const arr = new Array(Math.max(weeks,1)).fill(0)
    for (const step of plan.sequence) {
      const weeksSpan = Math.max(1, step.end_week - step.start_week + 1)
      const perWeek = step.est_hours / weeksSpan
      for (let w=step.start_week; w<=step.end_week; w++) {
        arr[w-1] += perWeek
      }
    }
    return arr.map(x=>Math.round(x))
  }

  function cumulative(arr:number[]): number[] { 
    const out:number[]=[]; 
    let acc=0; 
    for(const x of arr){ 
      acc+=x; 
      out.push(acc)
    } 
    return out 
  }

  function remainingFrom(plannedByWeek:number[], actual:number[]): {planned:number[], actual:number[]} {
    const total = plannedByWeek.reduce((a,b)=>a+b,0)
    const plannedCum = cumulative(plannedByWeek)
    const actualCum = cumulative(actual)
    const W = Math.max(plannedByWeek.length, actual.length)
    const plannedRem:number[] = []
    const actualRem:number[] = []
    for (let i=0;i<W;i++){
      const p = i<plannedCum.length ? plannedCum[i] : plannedCum[plannedCum.length-1]
      const a = i<actualCum.length ? actualCum[i] : actualCum[actualCum.length-1]||0
      plannedRem.push(Math.max(0, Math.round(total - p)))
      actualRem.push(Math.max(0, Math.round(total - a)))
    }
    return { planned: plannedRem, actual: actualRem }
  }

  function setActualForWeek(week:number, hours:number){
    setActualByWeek(prev => {
      const arr = prev.slice()
      for (let i=arr.length; i<week; i++) arr.push(0)
      arr[week-1] = Math.max(0, hours)
      return arr
    })
  }

  async function generate() {
    setLoading(true); 
    setError(null); 
    setPlan(null)
    
    try {
      const res = await fetch('http://127.0.0.1:8000/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          major: mode==='major'?major:null,
          role: mode==='role'?role:null,
          horizon_months: months,
          weekly_hours: weekly,
          budget,
          baseline_mastered: baseline.split(',').map(s=>s.trim()).filter(Boolean),
          w_time: wTime, 
          w_cost: wCost, 
          w_quality: wQuality,
          w_difficulty: wDifficulty,
          prefer_formats: preferFormats,
          variant: variant || null
        })
      })
      
      if (!res.ok) throw new Error('Planner error')
      const data = await res.json()
      setPlan(data)
      setActiveTab('roadmap')
      
      // Save for comparison
      if (data && comparePlans.length < 3) {
        setComparePlans([...comparePlans, {
          ...data,
          label: `${mode==='role'?role:major} - ${variant || 'custom'}`,
          timestamp: new Date().toISOString()
        }])
      }
    } catch (e:any) {
      setError(e.message || 'Error generating plan')
    } finally {
      setLoading(false)
    }
  }

  async function startQuiz() {
    setQuizItems(null); 
    setQuizResult(null); 
    setQuizAnswers({})
    
    const mj = mode==='role' ? 
      (role.includes('engineer') && !role.includes('software') ? 'ee' : 
       role.includes('journalist') ? 'communications' : 
       role.includes('health') ? 'public_health' : 'cs') 
      : major
    
    try {
      const res = await fetch('http://127.0.0.1:8000/quiz/start', {
        method:'POST', 
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ major: mj, num_items: 3 })
      })
      const data = await res.json()
      setQuizItems(data.items)
      setActiveTab('quiz')
    } catch (err) {
      console.error('Failed to start quiz:', err)
    }
  }

  async function gradeQuiz() {
    const mj = mode==='role' ? 
      (role.includes('engineer') && !role.includes('software') ? 'ee' : 
       role.includes('journalist') ? 'communications' : 
       role.includes('health') ? 'public_health' : 'cs') 
      : major
      
    try {
      const res = await fetch('http://127.0.0.1:8000/quiz/grade', {
        method:'POST', 
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ major: mj, answers: quizAnswers })
      })
      const data = await res.json()
      setQuizResult(data)
      
      if (data.inferred_mastered?.length) {
        const merged = Array.from(new Set(
          baseline.split(',').map(s=>s.trim()).filter(Boolean).concat(data.inferred_mastered)
        ))
        setBaseline(merged.join(', '))
      }
    } catch (err) {
      console.error('Failed to grade quiz:', err)
    }
  }

  async function saveProgress() {
    const progressData = {
      plan,
      actualByWeek,
      currentWeek,
      timestamp: new Date().toISOString()
    }
    
    try {
      await fetch('http://127.0.0.1:8000/progress/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(progressData)
      })
      alert('Progress saved!')
    } catch (err) {
      console.error('Failed to save progress:', err)
    }
  }

  async function loadProgress() {
    try {
      const res = await fetch('http://127.0.0.1:8000/progress/load')
      const data = await res.json()
      if (data.ok && data.data) {
        if (data.data.plan) setPlan(data.data.plan)
        if (data.data.actualByWeek) setActualByWeek(data.data.actualByWeek)
        if (data.data.currentWeek) setCurrentWeek(data.data.currentWeek)
        alert('Progress loaded!')
      }
    } catch (err) {
      console.error('Failed to load progress:', err)
    }
  }

  return (
    <div className="fade-in">
      <h1>🚀 AI Path Advisor Pro</h1>
      <p className="small">Advanced learning path planner with ILP optimization, quiz assessment, and progress tracking</p>
      
      <div className="tabs">
        <button className={`tab ${activeTab === 'config' ? 'active' : ''}`} onClick={()=>setActiveTab('config')}>
          📋 Configuration
        </button>
        <button className={`tab ${activeTab === 'quiz' ? 'active' : ''}`} onClick={()=>setActiveTab('quiz')}>
          🎯 Quiz Assessment
        </button>
        <button className={`tab ${activeTab === 'roadmap' ? 'active' : ''}`} onClick={()=>setActiveTab('roadmap')}>
          🗺️ Roadmap
        </button>
        <button className={`tab ${activeTab === 'progress' ? 'active' : ''}`} onClick={()=>setActiveTab('progress')}>
          📊 Progress
        </button>
      </div>

      {activeTab === 'config' && (
        <div className="grid">
          <div className="card">
            <h3>🎯 Target Configuration</h3>
            
            <label>Mode</label>
            <select value={mode} onChange={e=>setMode(e.target.value as any)}>
              <option value="role">Career Role</option>
              <option value="major">Academic Major</option>
            </select>

            {mode==='major' ? (
              <>
                <label>Major</label>
                <select value={major} onChange={e=>setMajor(e.target.value)}>
                  {['cs','ee','physics','public_health','materials','medicine','nursing','pharmacy','nutrition','me','civil','chemeng','environment','bme','law','policy','economics','education','architecture','communications'].map(m => (
                    <option key={m} value={m}>{m.toUpperCase()}</option>
                  ))}
                </select>
              </>
            ) : (
              <>
                <label>Career Role</label>
                <select value={role} onChange={e=>setRole(e.target.value)}>
                  {roles.map(r => <option key={r.key} value={r.key}>{r.name}</option>)}
                </select>
              </>
            )}

            <label>Study Duration (months)</label>
            <input type="number" value={months} onChange={e=>setMonths(parseInt(e.target.value||'0'))} />

            <label>Weekly Hours</label>
            <input type="number" value={weekly} onChange={e=>setWeekly(parseInt(e.target.value||'0'))} />

            <label>Budget ($)</label>
            <input type="number" value={budget} onChange={e=>setBudget(parseInt(e.target.value||'0'))} />

            <label>Baseline Skills (comma-separated)</label>
            <textarea 
              rows={2} 
              value={baseline} 
              onChange={e=>setBaseline(e.target.value)} 
              placeholder="e.g., prog.python.basics, math.calculus_1"
            />

            <label>Preferred Formats</label>
            <div style={{display:'flex', flexWrap:'wrap', gap:8, marginTop:8}}>
              {['video','text','problems','labs','projects','practice'].map(fmt => (
                <label key={fmt} style={{display:'flex', alignItems:'center', cursor:'pointer'}}>
                  <input 
                    type="checkbox" 
                    checked={preferFormats.includes(fmt)} 
                    onChange={e=>{
                      if (e.target.checked) setPreferFormats([...preferFormats, fmt])
                      else setPreferFormats(preferFormats.filter(f=>f!==fmt))
                    }} 
                  /> 
                  {fmt}
                </label>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>⚙️ Optimization Weights</h3>
            
            <label>Optimization Variant</label>
            <select value={variant} onChange={e=>setVariant(e.target.value as any)}>
              <option value="">Custom Weights</option>
              <option value="balanced">Balanced</option>
              <option value="fastest">Fastest</option>
              <option value="cheapest">Cheapest</option>
            </select>

            <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, marginTop:16}}>
              <div>
                <label>Time Weight</label>
                <input type="number" step="0.1" value={wTime} onChange={e=>setWTime(parseFloat(e.target.value||'1'))} />
              </div>
              <div>
                <label>Cost Weight</label>
                <input type="number" step="0.1" value={wCost} onChange={e=>setWCost(parseFloat(e.target.value||'0.5'))} />
              </div>
              <div>
                <label>Quality Weight</label>
                <input type="number" step="0.1" value={wQuality} onChange={e=>setWQuality(parseFloat(e.target.value||'1'))} />
              </div>
              <div>
                <label>Difficulty Weight</label>
                <input type="number" step="0.1" value={wDifficulty} onChange={e=>setWDifficulty(parseFloat(e.target.value||'0.1'))} />
              </div>
            </div>

            <div style={{display:'flex', gap:8, flexWrap:'wrap', marginTop:20}}>
              <button onClick={generate} disabled={loading}>
                {loading ? '⏳ Planning...' : '🚀 Generate Roadmap'}
              </button>
              <button className="secondary" onClick={startQuiz}>
                🎯 Take Quiz
              </button>
            </div>

            <div style={{marginTop:20, display:'flex', gap:8, flexWrap:'wrap'}}>
              <button onClick={()=>{setVariant('fastest'); generate();}}>⚡ Fastest</button>
              <button onClick={()=>{setVariant('cheapest'); generate();}}>💰 Cheapest</button>
              <button onClick={()=>{setVariant('balanced'); generate();}}>⚖️ Balanced</button>
            </div>

            {error && (
              <div style={{marginTop:16, padding:12, background:'#fed7d7', borderRadius:8, color:'#c53030'}}>
                ⚠️ {error}
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'quiz' && (
        <div className="card">
          <h3>🎯 Baseline Assessment Quiz</h3>
          
          {!quizItems && (
            <div>
              <p>Take a quick quiz to assess your current knowledge level.</p>
              <button onClick={startQuiz}>Start Quiz</button>
            </div>
          )}
          
          {quizItems && !quizResult && (
            <div>
              {quizItems.map((it, i) => (
                <div key={i} style={{marginBottom:20, padding:16, background:'#f7fafc', borderRadius:8}}>
                  <div style={{fontWeight:600, marginBottom:12}}>
                    Question {i+1}: {it.question}
                  </div>
                  <div>
                    {it.choices.map((c:string, j:number) => (
                      <label key={j} style={{display:'block', marginTop:8, cursor:'pointer'}}>
                        <input 
                          type="radio" 
                          name={`q${i}`} 
                          onChange={()=>setQuizAnswers({...quizAnswers, [i]: j})} 
                          checked={quizAnswers[i]===j} 
                        /> 
                        {c}
                      </label>
                    ))}
                  </div>
                </div>
              ))}
              <button onClick={gradeQuiz}>Submit Answers</button>
            </div>
          )}
          
          {quizResult && (
            <div style={{marginTop:20}}>
              <div className="stat-grid">
                <div className="stat-card">
                  <div className="stat-value">{quizResult.score}/{quizResult.total}</div>
                  <div className="stat-label">Score</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{Math.round((quizResult.score/quizResult.total)*100)}%</div>
                  <div className="stat-label">Percentage</div>
                </div>
              </div>
              
              {quizResult.inferred_mastered?.length > 0 && (
                <div style={{marginTop:16}}>
                  <strong>Mastered Skills Added:</strong>
                  <div style={{marginTop:8}}>
                    {quizResult.inferred_mastered.map((s:string) => (
                      <span key={s} className="badge secondary">{s}</span>
                    ))}
                  </div>
                </div>
              )}
              
              <button onClick={startQuiz} style={{marginTop:16}}>Retake Quiz</button>
            </div>
          )}
        </div>
      )}

      {activeTab === 'roadmap' && (
        <div>
          {!plan ? (
            <div className="card">
              <p>Generate a roadmap first to see your learning plan.</p>
            </div>
          ) : (
            <>
              <div className="card">
                <h3>📋 Roadmap Summary</h3>
                <div className="stat-grid">
                  <div className="stat-card">
                    <div className="stat-value">{plan.summary.weeks_total}</div>
                    <div className="stat-label">Total Weeks</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{plan.summary.weekly_hours}</div>
                    <div className="stat-label">Hours/Week</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">${plan.summary.budget_left}</div>
                    <div className="stat-label">Budget Left</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{plan.sequence.length}</div>
                    <div className="stat-label">Skills</div>
                  </div>
                </div>
                
                <div style={{marginTop:16}}>
                  {plan.summary.role && <span className="badge">{plan.summary.role}</span>}
                  {plan.summary.major && <span className="badge">{plan.summary.major}</span>}
                  {plan.summary.preferences?.map((p:string) => (
                    <span key={p} className="badge secondary">{p}</span>
                  ))}
                </div>

                <div style={{marginTop:16, display:'flex', gap:8}}>
                  <a 
                    href={`http://127.0.0.1:8000/export/ics?${mode==='major'?('major='+major):('role='+role)}&weekly_hours=${plan.summary.weekly_hours}`} 
                    target="_blank" 
                    rel="noreferrer"
                  >
                    <button>📅 Export to Calendar</button>
                  </a>
                  <button onClick={saveProgress}>💾 Save Progress</button>
                </div>
              </div>

              <div className="card" style={{marginTop:20}}>
                <h3>🎯 Milestones</h3>
                {plan.milestones.map((m:any, i:number) => (
                  <div key={i} style={{padding:12, borderBottom:'1px solid #e2e8f0'}}>
                    <strong>Week {m.week}:</strong> {m.name}
                    {m.skill && <span className="badge" style={{marginLeft:8}}>{m.skill}</span>}
                  </div>
                ))}
              </div>

              <div className="card" style={{marginTop:20}}>
                <h3>📚 Learning Sequence</h3>
                <div style={{maxHeight:400, overflow:'auto'}}>
                  {plan.sequence.slice(0,15).map((step:any, i:number) => (
                    <div key={i} style={{padding:12, borderBottom:'1px solid #e2e8f0'}}>
                      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                        <div>
                          <strong>{step.skill_id}</strong>
                          <div className="small">
                            Weeks {step.start_week}-{step.end_week} • {step.est_hours} hours
                          </div>
                        </div>
                        <div>
                          {step.resources.map((r:string) => (
                            <span key={r} className="badge warning" style={{fontSize:10}}>{r}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                  {plan.sequence.length > 15 && (
                    <div style={{padding:12, textAlign:'center', color:'#718096'}}>
                      ... and {plan.sequence.length - 15} more skills
                    </div>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {activeTab === 'progress' && (
        <div className="card">
          <h3>📊 Progress Dashboard</h3>
          
          <div style={{display:'flex', gap:8, marginBottom:20}}>
            <button onClick={loadProgress}>📥 Load Saved Progress</button>
            <button onClick={saveProgress}>💾 Save Current Progress</button>
          </div>
          
          {!plan ? (
            <p>Generate a plan first to track progress.</p>
          ) : (() => {
            const planned = computePlannedByWeek(plan)
            const { planned: plannedRem, actual: actualRem } = remainingFrom(planned, actualByWeek)
            const weeks = planned.length
            const W = 640, H = 240, pad = 28
            const maxY = Math.max(...plannedRem, ...(actualRem.length?actualRem:[0])) || 1
            
            function pathFor(series:number[]): string {
              if (!series.length) return ''
              return series.map((y, i) => {
                const xPos = pad + (i/(Math.max(series.length-1,1))) * (W-2*pad)
                const yPos = H-pad - (y/maxY) * (H-2*pad)
                return `${i===0?'M':'L'}${xPos},${yPos}`
              }).join(' ')
            }
            
            const totalHours = planned.reduce((a,b)=>a+b,0)
            const completedHours = actualByWeek.reduce((a,b)=>a+b,0)
            const progressPercent = totalHours > 0 ? (completedHours/totalHours)*100 : 0

            return (
              <div>
                <div className="grid">
                  <div>
                    <label>Current Week</label>
                    <input 
                      type="number" 
                      value={currentWeek} 
                      onChange={e=>setCurrentWeek(parseInt(e.target.value||'1'))} 
                    />
                    
                    <label>Hours Studied This Week</label>
                    <input 
                      type="number" 
                      value={actualByWeek[currentWeek-1]||0} 
                      onChange={e=>setActualForWeek(currentWeek, parseInt(e.target.value||'0'))} 
                    />
                    
                    <div className="stat-grid" style={{marginTop:20}}>
                      <div className="stat-card">
                        <div className="stat-value">{totalHours}</div>
                        <div className="stat-label">Total Hours</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-value">{completedHours}</div>
                        <div className="stat-label">Completed</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-value">{plannedRem[currentWeek-1]||0}</div>
                        <div className="stat-label">Remaining</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-value">{Math.round(progressPercent)}%</div>
                        <div className="stat-label">Progress</div>
                      </div>
                    </div>
                    
                    <div className="progress-bar" style={{marginTop:20}}>
                      <div className="progress-fill" style={{width: `${progressPercent}%`}}></div>
                    </div>
                  </div>
                  
                  <div>
                    <h4>Burndown Chart</h4>
                    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{width:'100%', height:'auto'}}>
                      {/* Grid */}
                      <line x1={pad} y1={H-pad} x2={W-pad} y2={H-pad} stroke="#e2e8f0" />
                      <line x1={pad} y1={pad} x2={pad} y2={H-pad} stroke="#e2e8f0" />
                      
                      {/* Planned line */}
                      <path 
                        d={pathFor(plannedRem)} 
                        fill="none" 
                        stroke="#cbd5e0" 
                        strokeWidth="2"
                        strokeDasharray="5,5"
                      />
                      
                      {/* Actual line */}
                      {actualRem.length > 0 && (
                        <path 
                          d={pathFor(actualRem)} 
                          fill="none" 
                          stroke="#667eea" 
                          strokeWidth="3"
                        />
                      )}
                      
                      {/* Labels */}
                      <text x={pad} y={pad-8} style={{fontSize:12, fill:'#718096'}}>Hours</text>
                      <text x={W-pad-40} y={H-6} style={{fontSize:12, fill:'#718096'}}>Weeks</text>
                    </svg>
                    
                    <div style={{marginTop:12, display:'flex', gap:16, justifyContent:'center'}}>
                      <div style={{display:'flex', alignItems:'center', gap:4}}>
                        <div style={{width:20, height:3, background:'#cbd5e0', borderRadius:2}}></div>
                        <span className="small">Planned</span>
                      </div>
                      <div style={{display:'flex', alignItems:'center', gap:4}}>
                        <div style={{width:20, height:3, background:'#667eea', borderRadius:2}}></div>
                        <span className="small">Actual</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )
          })()}
        </div>
      )}

      {comparePlans.length > 0 && (
        <div className="card" style={{marginTop:20}}>
          <h3>📊 Plan Comparison</h3>
          <div style={{overflowX:'auto'}}>
            <table style={{width:'100%', borderCollapse:'collapse'}}>
              <thead>
                <tr style={{borderBottom:'2px solid #e2e8f0'}}>
                  <th style={{padding:8, textAlign:'left'}}>Plan</th>
                  <th style={{padding:8}}>Weeks</th>
                  <th style={{padding:8}}>Hours/Week</th>
                  <th style={{padding:8}}>Total Hours</th>
                  <th style={{padding:8}}>Budget Left</th>
                </tr>
              </thead>
              <tbody>
                {comparePlans.map((p, i) => (
                  <tr key={i} style={{borderBottom:'1px solid #e2e8f0'}}>
                    <td style={{padding:8}}>{p.label}</td>
                    <td style={{padding:8, textAlign:'center'}}>{p.summary.weeks_total}</td>
                    <td style={{padding:8, textAlign:'center'}}>{p.summary.weekly_hours}</td>
                    <td style={{padding:8, textAlign:'center'}}>
                      {p.summary.weeks_total * p.summary.weekly_hours}
                    </td>
                    <td style={{padding:8, textAlign:'center'}}>${p.summary.budget_left}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button 
            className="danger" 
            onClick={()=>setComparePlans([])} 
            style={{marginTop:12}}
          >
            Clear Comparisons
          </button>
        </div>
      )}
    </div>
  )
}