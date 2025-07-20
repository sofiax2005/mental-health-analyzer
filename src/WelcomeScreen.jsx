import { useEffect, useState } from "react";
import { Player } from "@lottiefiles/react-lottie-player";
import { motion, AnimatePresence } from "framer-motion";
import welcomeAnim from "https://lottie.host/ea66c74d-b136-4022-a495-cd16aa4c7b3c/1iZFMdhkMp.json"; // replace with your actual path

function Analyser() {
  const [showWelcome, setShowWelcome] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 4000); // adjust to your lottie duration

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative w-full h-screen bg-white">
      <AnimatePresence>
        {showWelcome && (
          <motion.div
            key="welcome"
            className="absolute inset-0 flex items-center justify-center bg-white z-50"
            initial={{ opacity: 1 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 1.5 }}
          >
            <Player
              autoplay
              keepLastFrame
              src={welcomeAnim}
              style={{ height: "60%", width: "60%" }}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main UI goes here */}
      {!showWelcome && (
        <motion.div
          className="z-0 p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.5 }}
        >
          <h1 className="text-3xl font-bold mb-4">Mood Analyzer</h1>
          {/* Your journaling UI, graphs, whatever */}
        </motion.div>
      )}
    </div>
  );
}

export default Analyser;
