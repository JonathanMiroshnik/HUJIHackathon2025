import { useState } from 'react';
import './MemoryCard.css'

interface MemoryCardProps {
    word: string;
}

function MemoryCard({ word }: MemoryCardProps) {

    return (
        <div>
            { word }
        </div>
    );
}

export default MemoryCard;