'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './Card';
import { Button } from './Button';
import { Textarea } from './Textarea';
import { Select } from './Select';
import { translationApi } from '@/lib/api';
import { TranslationResponse, LanguageInfo, ApiError } from '@/lib/types';
import { formatTime, detectLanguage, copyToClipboard, isValidText } from '@/lib/utils';
import { ArrowRightLeft, Copy, RotateCcw, Loader2, CheckCircle } from 'lucide-react';

export default function TranslationForm() {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('ta');
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [languages, setLanguages] = useState<LanguageInfo[]>([]);
  const [lastTranslation, setLastTranslation] = useState<TranslationResponse | null>(null);
  const [copySuccess, setCopySuccess] = useState(false);

  // Advanced options
  const [numBeams, setNumBeams] = useState(4);
  const [maxLength, setMaxLength] = useState(512);
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Load supported languages on mount
  useEffect(() => {
    const loadLanguages = async () => {
      try {
        const response = await translationApi.getSupportedLanguages();
        setLanguages(response.languages);
      } catch (err) {
        console.error('Failed to load languages:', err);
        // Fallback languages
        setLanguages([
          { code: 'en', name: 'English', native_name: 'English' },
          { code: 'ta', name: 'Tamil', native_name: 'தமிழ்' }
        ]);
      }
    };
    loadLanguages();
  }, []);

  // Auto-detect language on input change
  useEffect(() => {
    if (inputText.trim()) {
      const detected = detectLanguage(inputText);
      if (detected !== 'unknown' && detected !== sourceLanguage) {
        setSourceLanguage(detected);
        setTargetLanguage(detected === 'en' ? 'ta' : 'en');
      }
    }
  }, [inputText, sourceLanguage]);

  const handleTranslate = async () => {
    if (!isValidText(inputText)) {
      setError('Please enter valid text (1-1000 characters)');
      return;
    }

    setIsTranslating(true);
    setError(null);

    try {
      const response = await translationApi.translate({
        text: inputText,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        num_beams: numBeams,
        max_length: maxLength
      });

      setTranslatedText(response.translated_text);
      setLastTranslation(response);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Translation failed. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  const handleSwapLanguages = () => {
    setSourceLanguage(targetLanguage);
    setTargetLanguage(sourceLanguage);
    setInputText(translatedText);
    setTranslatedText(inputText);
  };

  const handleClear = () => {
    setInputText('');
    setTranslatedText('');
    setError(null);
    setLastTranslation(null);
  };

  const handleCopyToClipboard = async () => {
    if (translatedText) {
      try {
        await copyToClipboard(translatedText);
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      } catch (err) {
        console.error('Failed to copy text:', err);
      }
    }
  };

  const languageOptions = languages.map(lang => ({
    value: lang.code,
    label: `${lang.name} (${lang.native_name})`
  }));

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center text-gray-800">
          Neural Machine Translation
        </CardTitle>
        <p className="text-center text-gray-600">
          English ↔ Tamil Translation using AI
        </p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Language Selection */}
        <div className="flex items-center justify-center gap-4">
          <Select
            label="From"
            value={sourceLanguage}
            onChange={(e) => setSourceLanguage(e.target.value)}
            options={languageOptions}
            className="w-48"
          />
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleSwapLanguages}
            className="mt-6"
            disabled={isTranslating}
          >
            <ArrowRightLeft className="w-4 h-4" />
          </Button>
          
          <Select
            label="To"
            value={targetLanguage}
            onChange={(e) => setTargetLanguage(e.target.value)}
            options={languageOptions}
            className="w-48"
          />
        </div>

        {/* Input and Output */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input */}
          <div className="space-y-4">
            <Textarea
              label="Enter text to translate"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your text here..."
              className="min-h-[200px]"
              maxLength={1000}
              error={error ?? undefined}
            />
            <div className="flex justify-between items-center text-sm text-gray-500">
              <span>{inputText.length}/1000 characters</span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleClear}
                disabled={isTranslating}
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Clear
              </Button>
            </div>
          </div>

          {/* Output */}
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">
                Translation
              </label>
              <div className="relative">
                <div className="flex min-h-[200px] w-full rounded-md border border-gray-300 bg-gray-50 px-3 py-2 text-sm">
                  {translatedText ? (
                    <div className="flex-1">
                      {translatedText}
                    </div>
                  ) : (
                    <div className="flex-1 text-gray-400">
                      Translation will appear here...
                    </div>
                  )}
                </div>
                {translatedText && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="absolute top-2 right-2"
                    onClick={handleCopyToClipboard}
                  >
                    {copySuccess ? (
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </Button>
                )}
              </div>
            </div>

            {/* Translation Stats */}
            {lastTranslation && (
              <div className="text-sm text-gray-500 space-y-1">
                <div>Processing time: {formatTime(lastTranslation.processing_time_ms)}</div>
                <div>Characters translated: {lastTranslation.original_text.length}</div>
              </div>
            )}
          </div>
        </div>

        {/* Advanced Options */}
        <div className="space-y-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-blue-600"
          >
            {showAdvanced ? 'Hide' : 'Show'} Advanced Options
          </Button>
          
          {showAdvanced && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  Number of Beams: {numBeams}
                </label>
                <input
                  type="range"
                  min={1}
                  max={10}
                  value={numBeams}
                  onChange={(e) => setNumBeams(parseInt(e.target.value))}
                  className="w-full"
                  title="Number of beams for translation"
                />
                <p className="text-xs text-gray-500">
                  Higher values may produce better translations but take longer
                </p>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  Max Length: {maxLength}
                </label>
                <input
                  type="range"
                  min={128}
                  max={1024}
                  step={64}
                  value={maxLength}
                  onChange={(e) => setMaxLength(parseInt(e.target.value))}
                  className="w-full"
                  title="Maximum length of translated text"
                />
                <p className="text-xs text-gray-500">
                  Maximum length of the translated text
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Translate Button */}
        <div className="flex justify-center">
          <Button
            onClick={handleTranslate}
            disabled={isTranslating || !inputText.trim()}
            className="w-full md:w-auto md:px-8"
          >
            {isTranslating ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Translating...
              </>
            ) : (
              'Translate'
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
