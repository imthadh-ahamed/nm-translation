'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './Card';
import { Button } from './Button';
import { translationApi } from '@/lib/api';
import { HealthResponse, ApiError } from '@/lib/types';
import { Loader2, CheckCircle, XCircle, RefreshCw, Server } from 'lucide-react';

export default function HealthStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await translationApi.getHealth();
      setHealth(response);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'Failed to check health');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  const renderContent = () => {
    if (isLoading && !health) {
      return (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin mr-2" />
          Checking system health...
        </div>
      );
    }

    if (error) {
      return (
        <div className="text-center py-8 space-y-4">
          <XCircle className="w-12 h-12 text-red-500 mx-auto" />
          <div className="text-red-600">{error}</div>
          <Button onClick={checkHealth} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </div>
      );
    }

    if (!health) {
      return null;
    }

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            {health.status === 'healthy' ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : (
              <XCircle className="w-5 h-5 text-red-600" />
            )}
            <div>
              <div className="font-medium">Service Status</div>
              <div className={`text-sm capitalize ${
                health.status === 'healthy' ? 'text-green-600' : 'text-red-600'
              }`}>
                {health.status}
              </div>
            </div>
          </div>
          <Button onClick={checkHealth} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4" />
          </Button>
        </div>

        <div className="p-4 border rounded-lg">
          <div className="font-medium mb-2">Model Information</div>
          <div className="space-y-1 text-sm">
            <div>Status: {health.model_loaded ? 'Loaded' : 'Loading'}</div>
            <div>Version: {health.version}</div>
            {health.model_info && (
              <>
                <div>Name: {health.model_info.name}</div>
                <div>Device: {health.model_info.device}</div>
              </>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Server className="w-5 h-5" />
          System Health
        </CardTitle>
      </CardHeader>
      
      <CardContent>
        {renderContent()}
      </CardContent>
    </Card>
  );
}
