import { GoogleGenAI } from "@google/genai";

const apiKey = process.env.API_KEY || '';
// Initialize conditionally to prevent crashes if no key is present during initial render
let ai: GoogleGenAI | null = null;

if (apiKey) {
  ai = new GoogleGenAI({ apiKey });
}

export const analyzeAccidentReport = async (description: string): Promise<{ severity: string, summary: string }> => {
  if (!ai) return { severity: 'Unknown', summary: 'AI service unavailable' };

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: `Analyze the following accident description and provide a JSON response with a predicted severity (Low, Medium, High, Critical) and a short one-sentence summary. Description: "${description}"`,
      config: {
        responseMimeType: 'application/json'
      }
    });
    
    const text = response.text || '{}';
    return JSON.parse(text);
  } catch (error) {
    console.error("Gemini Analysis Error:", error);
    return { severity: 'Unknown', summary: 'Could not analyze.' };
  }
};

export const getSafetyAdvice = async (topic: string): Promise<string> => {
  if (!ai) return "AI service unavailable. Please check official traffic rules.";

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: `Provide a short, concise, and helpful road safety tip regarding: "${topic}". Keep it under 50 words.`,
    });
    return response.text || "Drive safely.";
  } catch (error) {
    console.error("Gemini Advice Error:", error);
    return "Always follow traffic signals and signs.";
  }
};