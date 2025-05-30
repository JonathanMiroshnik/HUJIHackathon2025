import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { LanguageSpeech } from '../components/SpeechBubble/SpeechBubble';

interface AppContextType {
  // MainPage state
  currentView: string;
  setCurrentView: (view: string) => void;
  
  // Conversation with student
  conversation: LanguageSpeech[][],
  setConversation: (conv: LanguageSpeech[][]) => void,
  addConversation: (curConvo: LanguageSpeech[]) => void,

  // Student state
  student: StudentState,
  setStudent: (curStudent: StudentState) => void,

  // MemoryPage state
  memoryWords: string[];
  setMemoryWords: (words: string[]) => void;
  addMemoryWord: (word: string) => void;
  removeMemoryWord: (word: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

interface AppProviderProps {
  children: ReactNode;
}

export interface StudentState {
  name: string;
  age: string;
  gender: string;
  background_info: string;
  arabic_proficiency_level: string;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const INITIAL_CONVERSATION = {
    text: "שלום, אני המורה הווירטואלית שלכם לערבית, בואו ביחד ונלמד للغة العربية",
    language: "Hebrew"
  };
  const [conversation, setConversation] = useState<LanguageSpeech[][]>([[INITIAL_CONVERSATION]]);

  const addConversation = (curConvo: LanguageSpeech[]) => {
    setConversation(prev => [...prev.map((p) => [...p]), [...curConvo]]);
  };

  const [student, setStudent] = useState<StudentState>({
    name: "",
    age: "",
    gender: "",
    background_info: "",
    arabic_proficiency_level: ""
  });

  // const removeConversation = (word: string) => {
  //   setMemoryWords(prev => prev.filter(w => w !== word));
  // };

  const [currentView, setCurrentView] = useState('dashboard');
  const [memoryWords, setMemoryWords] = useState<string[]>([]);  

  const addMemoryWord = (word: string) => {
    setMemoryWords(prev => [...prev, word]);
  };

  const removeMemoryWord = (word: string) => {
    setMemoryWords(prev => prev.filter(w => w !== word));
  };

  return (
    <AppContext.Provider value={{
      currentView,
      setCurrentView,
      conversation,
      setConversation,
      addConversation,
      student,
      setStudent,
      memoryWords,
      setMemoryWords,
      addMemoryWord,
      removeMemoryWord
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
