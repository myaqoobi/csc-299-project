import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { text, tone } = await request.json()

    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { error: 'Text is required' },
        { status: 400 }
      )
    }

    // For now, we'll use a simple text transformation
    // In production, you'd integrate with AI services like OpenAI, Anthropic, etc.
    const humanizedText = await humanizeText(text, tone)

    return NextResponse.json({
      humanizedText,
      originalLength: text.length,
      humanizedLength: humanizedText.length
    })

  } catch (error) {
    console.error('Error in humanize API:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

async function humanizeText(text: string, tone: string): Promise<string> {
  // Enhanced humanization with more sophisticated transformations
  let humanized = text

  // 1. Replace AI-typical phrases with more natural alternatives
  const aiPhraseReplacements = [
    { from: /\bIt is important to note that\b/gi, to: 'Keep in mind that' },
    { from: /\bFurthermore\b/gi, to: 'Also' },
    { from: /\bMoreover\b/gi, to: 'Plus' },
    { from: /\bAdditionally\b/gi, to: 'And' },
    { from: /\bIn conclusion\b/gi, to: 'To wrap up' },
    { from: /\bIt should be noted that\b/gi, to: 'Remember that' },
    { from: /\bIt is worth mentioning that\b/gi, to: "It's worth noting" },
    { from: /\bAs a result\b/gi, to: 'So' },
    { from: /\bTherefore\b/gi, to: "That's why" },
    { from: /\bHowever\b/gi, to: 'But' },
    { from: /\bNevertheless\b/gi, to: 'Still' },
    { from: /\bIn addition\b/gi, to: 'Plus' },
    { from: /\bFor instance\b/gi, to: 'For example' },
    { from: /\bIn order to\b/gi, to: 'To' },
    { from: /\bDue to the fact that\b/gi, to: 'Because' },
    { from: /\bIn the event that\b/gi, to: 'If' },
    { from: /\bAt this point in time\b/gi, to: 'Now' },
    { from: /\bPrior to\b/gi, to: 'Before' },
    { from: /\bSubsequent to\b/gi, to: 'After' },
    { from: /\bWith regard to\b/gi, to: 'About' },
    { from: /\bIn terms of\b/gi, to: 'When it comes to' },
    { from: /\bIt is evident that\b/gi, to: 'Clearly' },
    { from: /\bIt is clear that\b/gi, to: 'Obviously' },
    { from: /\bIt is apparent that\b/gi, to: 'It seems' },
    { from: /\bIt can be seen that\b/gi, to: 'You can see that' },
    { from: /\bIt should be emphasized that\b/gi, to: 'It\'s crucial to note' },
    { from: /\bIn other words\b/gi, to: 'Put simply' },
    { from: /\bTo put it simply\b/gi, to: 'Basically' },
    { from: /\bNeedless to say\b/gi, to: 'Obviously' },
    { from: /\bLast but not least\b/gi, to: 'Finally' },
    { from: /\bFirst and foremost\b/gi, to: 'First' },
    { from: /\bOn the other hand\b/gi, to: 'Meanwhile' },
    { from: /\bAt the same time\b/gi, to: 'Also' },
    { from: /\bIn the meantime\b/gi, to: 'Meanwhile' },
    { from: /\bAs mentioned above\b/gi, to: 'As I said' },
    { from: /\bAs stated previously\b/gi, to: 'Like I mentioned' },
    { from: /\bIn the following section\b/gi, to: 'Next' },
    { from: /\bIn the previous section\b/gi, to: 'Before' },
    { from: /\bIt is recommended that\b/gi, to: 'You should' },
    { from: /\bIt is suggested that\b/gi, to: 'Consider' },
    { from: /\bIt is advised that\b/gi, to: 'Try to' }
  ]

  // Apply AI phrase replacements
  aiPhraseReplacements.forEach(({ from, to }) => {
    humanized = humanized.replace(from, to)
  })

  // 2. Sentence restructuring and variation
  const sentences = humanized.split(/[.!?]+/).filter(s => s.trim())
  if (sentences.length > 1) {
    const variedSentences = sentences.map((sentence, index) => {
      sentence = sentence.trim()
      if (!sentence) return ''
      
      // Add natural sentence starters for variety
      const casualStarters = ['Also', 'Plus', 'And', 'But', 'So', 'Now', "Here's the thing", 'By the way', 'Actually', 'Really', 'Honestly']
      const formalStarters = ['Additionally', 'Furthermore', 'Moreover', 'However', 'Nevertheless', 'Consequently', 'Accordingly', 'Subsequently']
      const creativeStarters = ['Interestingly', 'Surprisingly', 'Amazingly', 'Remarkably', 'Fascinatingly', 'Intriguingly', 'Remarkably']
      
      if (index > 0 && Math.random() > 0.6 && sentence.length > 15) {
        let starter = ''
        switch (tone) {
          case 'casual':
            starter = casualStarters[Math.floor(Math.random() * casualStarters.length)]
            break
          case 'formal':
            starter = formalStarters[Math.floor(Math.random() * formalStarters.length)]
            break
          case 'creative':
            starter = creativeStarters[Math.floor(Math.random() * creativeStarters.length)]
            break
          default:
            starter = casualStarters[Math.floor(Math.random() * casualStarters.length)]
        }
        
        if (tone === 'casual') {
          return `${starter.toLowerCase()}, ${sentence.toLowerCase()}`
        } else {
          return `${starter}, ${sentence.toLowerCase()}`
        }
      }
      return sentence
    }).filter(s => s)
    
    humanized = variedSentences.join('. ') + '.'
  }

  // 3. Tone-specific transformations
  switch (tone) {
    case 'casual':
      humanized = humanized
        .replace(/\bI will\b/gi, "I'll")
        .replace(/\bwe will\b/gi, "we'll")
        .replace(/\bdo not\b/gi, "don't")
        .replace(/\bdoes not\b/gi, "doesn't")
        .replace(/\bcannot\b/gi, "can't")
        .replace(/\bwould not\b/gi, "wouldn't")
        .replace(/\bshould not\b/gi, "shouldn't")
        .replace(/\bwill not\b/gi, "won't")
        .replace(/\bcould not\b/gi, "couldn't")
        .replace(/\bhave not\b/gi, "haven't")
        .replace(/\bhas not\b/gi, "hasn't")
        .replace(/\bhad not\b/gi, "hadn't")
        .replace(/\bis not\b/gi, "isn't")
        .replace(/\bare not\b/gi, "aren't")
        .replace(/\bwas not\b/gi, "wasn't")
        .replace(/\bwere not\b/gi, "weren't")
        .replace(/\bIt is\b/gi, "It's")
        .replace(/\bThat is\b/gi, "That's")
        .replace(/\bThere is\b/gi, "There's")
        .replace(/\bHere is\b/gi, "Here's")
        .replace(/\bWhat is\b/gi, "What's")
        .replace(/\bWho is\b/gi, "Who's")
        .replace(/\bWhere is\b/gi, "Where's")
        .replace(/\bWhen is\b/gi, "When's")
        .replace(/\bHow is\b/gi, "How's")
        .replace(/\bWhy is\b/gi, "Why's")
        break
    
    case 'formal':
      humanized = humanized
        .replace(/\bdon't\b/gi, 'do not')
        .replace(/\bdoesn't\b/gi, 'does not')
        .replace(/\bcan't\b/gi, 'cannot')
        .replace(/\bwon't\b/gi, 'will not')
        .replace(/\bshouldn't\b/gi, 'should not')
        .replace(/\bwouldn't\b/gi, 'would not')
        .replace(/\bcouldn't\b/gi, 'could not')
        .replace(/\bhaven't\b/gi, 'have not')
        .replace(/\bhasn't\b/gi, 'has not')
        .replace(/\bhadn't\b/gi, 'had not')
        .replace(/\bisn't\b/gi, 'is not')
        .replace(/\baren't\b/gi, 'are not')
        .replace(/\bwasn't\b/gi, 'was not')
        .replace(/\bweren't\b/gi, 'were not')
        .replace(/\bIt's\b/gi, 'It is')
        .replace(/\bThat's\b/gi, 'That is')
        .replace(/\bThere's\b/gi, 'There is')
        .replace(/\bHere's\b/gi, 'Here is')
        .replace(/\bWhat's\b/gi, 'What is')
        .replace(/\bWho's\b/gi, 'Who is')
        .replace(/\bWhere's\b/gi, 'Where is')
        .replace(/\bWhen's\b/gi, 'When is')
        .replace(/\bHow's\b/gi, 'How is')
        .replace(/\bWhy's\b/gi, 'Why is')
        break
  }

  // 4. Enhanced synonym replacement with context awareness
  const synonyms: { [key: string]: string[] } = {
    'good': ['great', 'excellent', 'fantastic', 'awesome', 'amazing', 'wonderful', 'outstanding'],
    'bad': ['terrible', 'awful', 'horrible', 'poor', 'dreadful', 'atrocious', 'lousy'],
    'big': ['large', 'huge', 'massive', 'enormous', 'gigantic', 'colossal', 'substantial'],
    'small': ['tiny', 'little', 'miniature', 'compact', 'petite', 'minuscule', 'diminutive'],
    'important': ['crucial', 'vital', 'essential', 'key', 'critical', 'significant', 'paramount'],
    'interesting': ['fascinating', 'intriguing', 'compelling', 'engaging', 'captivating', 'absorbing'],
    'very': ['really', 'quite', 'extremely', 'incredibly', 'totally', 'absolutely'],
    'really': ['truly', 'genuinely', 'actually', 'definitely', 'certainly', 'absolutely'],
    'many': ['numerous', 'plenty of', 'a lot of', 'tons of', 'loads of', 'countless'],
    'some': ['a few', 'several', 'a handful of', 'a number of', 'various', 'certain'],
    'often': ['frequently', 'regularly', 'commonly', 'usually', 'typically', 'habitually'],
    'sometimes': ['occasionally', 'now and then', 'from time to time', 'periodically', 'intermittently'],
    'always': ['constantly', 'continuously', 'perpetually', 'invariably', 'consistently'],
    'never': ['not ever', 'at no time', 'under no circumstances', 'in no way'],
    'help': ['assist', 'aid', 'support', 'guide', 'facilitate', 'enable'],
    'make': ['create', 'produce', 'generate', 'build', 'construct', 'develop'],
    'use': ['utilize', 'employ', 'apply', 'leverage', 'harness', 'exploit'],
    'get': ['obtain', 'acquire', 'receive', 'gain', 'attain', 'secure'],
    'find': ['discover', 'locate', 'identify', 'uncover', 'detect', 'spot'],
    'show': ['demonstrate', 'reveal', 'display', 'exhibit', 'present', 'illustrate'],
    'think': ['believe', 'consider', 'contemplate', 'reflect', 'ponder', 'assess'],
    'know': ['understand', 'comprehend', 'recognize', 'realize', 'grasp', 'perceive'],
    'see': ['observe', 'notice', 'perceive', 'witness', 'view', 'behold'],
    'feel': ['sense', 'experience', 'perceive', 'detect', 'notice', 'observe'],
    'want': ['desire', 'wish for', 'crave', 'long for', 'yearn for', 'seek'],
    'need': ['require', 'demand', 'necessitate', 'call for', 'entail', 'involve'],
    'try': ['attempt', 'endeavor', 'strive', 'seek', 'aim', 'work towards'],
    'work': ['function', 'operate', 'perform', 'function', 'run', 'behave'],
    'start': ['begin', 'commence', 'initiate', 'launch', 'embark on', 'kick off'],
    'stop': ['cease', 'halt', 'discontinue', 'terminate', 'end', 'finish'],
    'change': ['alter', 'modify', 'transform', 'convert', 'adapt', 'adjust']
  }

  // Apply synonym replacements with some randomness
  for (const [word, alternatives] of Object.entries(synonyms)) {
    const regex = new RegExp(`\\b${word}\\b`, 'gi')
    const matches = humanized.match(regex)
    if (matches) {
      matches.forEach(() => {
        if (Math.random() > 0.5) { // 50% chance to replace each occurrence
          const replacement = alternatives[Math.floor(Math.random() * alternatives.length)]
          humanized = humanized.replace(regex, replacement)
        }
      })
    }
  }

  // 5. Add natural language patterns
  const naturalPatterns = [
    { from: /\bthe fact that\b/gi, to: 'that' },
    { from: /\bin the case of\b/gi, to: 'for' },
    { from: /\bwith respect to\b/gi, to: 'about' },
    { from: /\bin relation to\b/gi, to: 'about' },
    { from: /\bin accordance with\b/gi, to: 'following' },
    { from: /\bwith regard to\b/gi, to: 'about' },
    { from: /\bin terms of\b/gi, to: 'when it comes to' },
    { from: /\bin the context of\b/gi, to: 'for' },
    { from: /\bfrom the perspective of\b/gi, to: 'from' },
    { from: /\bon the basis of\b/gi, to: 'based on' },
    { from: /\bin the process of\b/gi, to: '' },
    { from: /\bin the course of\b/gi, to: 'during' },
    { from: /\bin the absence of\b/gi, to: 'without' },
    { from: /\bin the presence of\b/gi, to: 'with' },
    { from: /\bin the event of\b/gi, to: 'if' },
    { from: /\bin the context of\b/gi, to: 'for' },
    { from: /\bin the framework of\b/gi, to: 'in' },
    { from: /\bin the realm of\b/gi, to: 'in' },
    { from: /\bin the domain of\b/gi, to: 'in' },
    { from: /\bin the sphere of\b/gi, to: 'in' }
  ]

  naturalPatterns.forEach(({ from, to }) => {
    humanized = humanized.replace(from, to)
  })

  // 6. Add some randomness to sentence length and structure
  if (sentences.length > 2) {
    const finalSentences = humanized.split(/[.!?]+/).filter(s => s.trim())
    const variedFinalSentences = finalSentences.map((sentence, index) => {
      sentence = sentence.trim()
      
      // Sometimes combine short sentences
      if (sentence.length < 30 && index < finalSentences.length - 1 && Math.random() > 0.7) {
        const nextSentence = finalSentences[index + 1]?.trim()
        if (nextSentence && nextSentence.length < 30) {
          return `${sentence} and ${nextSentence.toLowerCase()}`
        }
      }
      
      // Sometimes split long sentences (simplified)
      if (sentence.length > 100 && sentence.includes(',') && Math.random() > 0.8) {
        const parts = sentence.split(',')
        if (parts.length > 1) {
          return parts[0] + '. ' + parts.slice(1).join(',').trim()
        }
      }
      
      return sentence
    }).filter(s => s)
    
    humanized = variedFinalSentences.join('. ') + '.'
  }

  return humanized.trim()
}

// Example integration with OpenAI (commented out - requires API key)
/*
async function humanizeWithOpenAI(text: string, tone: string): Promise<string> {
  const OpenAI = require('openai')
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  })

  const tonePrompts = {
    casual: "Rewrite this text in a casual, friendly, and conversational tone while maintaining the original meaning:",
    formal: "Rewrite this text in a formal, professional tone while maintaining the original meaning:",
    creative: "Rewrite this text in a creative, engaging, and compelling tone while maintaining the original meaning:",
    academic: "Rewrite this text in an academic, scholarly tone while maintaining the original meaning:"
  }

  const prompt = `${tonePrompts[tone]}\n\n${text}`

  const completion = await openai.chat.completions.create({
    messages: [{ role: "user", content: prompt }],
    model: "gpt-3.5-turbo",
    max_tokens: 1000,
    temperature: 0.7,
  })

  return completion.choices[0].message.content
}
*/
