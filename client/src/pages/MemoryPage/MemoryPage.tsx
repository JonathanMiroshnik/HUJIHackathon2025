import { useState } from 'react';
import MemoryCard from './MemoryCard/MemoryCard';
import './MemoryPage.css'

function MemoryPage() {
    const [words, setWords] = useState<string[]>(["hello", "lol"]);

    return (
        <div>
            { words.map((word, index) => 
                <div key={"memory_word_" + index}>
                    <MemoryCard word={word}/>
                </div>
            ) }
        </div>
    );
}

export default MemoryPage;