import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatTime(milliseconds: number): string {
  if (milliseconds < 1000) {
    return `${Math.round(milliseconds)}ms`;
  }
  return `${(milliseconds / 1000).toFixed(2)}s`;
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
}

export function detectLanguage(text: string): 'en' | 'ta' | 'unknown' {
  // Simple language detection based on character patterns
  const tamilPattern = /[\u0B80-\u0BFF]/;
  const englishPattern = /[a-zA-Z]/;
  
  if (tamilPattern.test(text)) {
    return 'ta';
  } else if (englishPattern.test(text)) {
    return 'en';
  }
  
  return 'unknown';
}

export function copyToClipboard(text: string): Promise<void> {
  return navigator.clipboard.writeText(text);
}

export function isValidText(text: string): boolean {
  return text.trim().length > 0 && text.trim().length <= 1000;
}
