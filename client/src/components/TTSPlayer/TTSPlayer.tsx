import React, { useState } from "react";
import { BACKEND_URL } from "../../config/constants";

const TTSPlayer: React.FC = () => {
  const [text, setText] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("text", text);

    const response = await fetch(BACKEND_URL + "tts", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      alert("Failed to fetch audio");
      return;
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);

    const audio = new Audio(audioUrl);
    audio.play();
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to speak"
        rows={4}
        cols={40}
      />
      <button type="submit">Speak</button>
    </form>
  );
};

export default TTSPlayer;
