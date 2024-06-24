export type EmotionLabels = "joy" | "sadness" | "anger" | "surprise" | "disgust" | "fear" | "others"
export type SentimentLabels = "POS" | "NEG" | "NEU"

const EmotionEmoticons = {
  "joy": "😊",
  "sadness": "😞",
  "anger": "😡",
  "surprise": "😲",
  "disgust": "🤢",
  "fear": "😱",
  "others": "😐",
}

export const getEmoji = (emotion: EmotionLabels, sentiment: SentimentLabels) => {
  if (!emotion.includes('others')) {
    return EmotionEmoticons[emotion]
  }

  return sentiment === "POS" ? "😊" : sentiment === "NEG" ? "😞" : "😐"
}