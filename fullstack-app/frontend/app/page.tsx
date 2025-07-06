import TranslationForm from '@/components/TranslationForm';
import HealthStatus from '@/components/HealthStatus';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900">
            Neural Machine Translation
          </h1>
          <p className="text-lg text-gray-600">
            English ↔ Tamil Translation powered by AI
          </p>
        </div>

        {/* Main Translation Interface */}
        <TranslationForm />

        {/* Health Status */}
        <HealthStatus />
      </div>
    </div>
  );
}
