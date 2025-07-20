import { useEffect, useState } from "react";
import Lottie from "lottie-react";
import welcomeAnim from "https://lottie.host/ea66c74d-b136-4022-a495-cd16aa4c7b3c/1iZFMdhkMp.json"; // your .json file

const WelcomeScreen = ({ onFinish }) => {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Wait for 3 seconds, then fade out
    const timer = setTimeout(() => setFadeOut(true), 3000);

    // Fully hide after fade-out transition
    const finishTimer = setTimeout(() => onFinish(), 4000);

    return () => {
      clearTimeout(timer);
      clearTimeout(finishTimer);
    };
  }, [onFinish]);

  return (
    <div
      className={`fixed inset-0 bg-white flex flex-col items-center justify-center transition-opacity duration-1000 z-50 ${
        fadeOut ? "opacity-0" : "opacity-100"
      }`}
    >
      <Lottie animationData={welcomeAnim} style={{ height: 250 }} />
      <p className="text-lg text-gray-600 mt-4">Welcome to your mood haven ✨</p>
    </div>
  );
};

export default WelcomeScreen;
