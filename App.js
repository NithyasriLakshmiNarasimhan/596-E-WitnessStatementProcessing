import React from 'react';
import './style.css';
import { useState } from 'react';

const highlightWords = (text, words) => {
  const wordArray = text.split(' ');


  const highlightedText = wordArray.map((word, index) => {
    const isHighlighted = words.some(item => word.toLowerCase().includes(item.toLowerCase()));
    
    return isHighlighted ? <span key={index} className="highlight">{word} </span> : <span key={index}>{word} </span>;
  });

  return highlightedText;
};


function App() {

  const [paragraph, setParagraph] = useState(
    "Statement 1: My name is Mark Wilson. I'm a bartender at Ressles's Pub downtown. Last night, around 11:30pm, I witnessed a fight break out between two male customers. They were shouting at each other and it quickly turned physical. The taller man slammed the other up against the wall and I saw him pull out a knife from his jacket. Before I could react, he stabbed the other man multiple times in the chest and stomach. Blood was everywhere. The victim collapsed to the ground. I yelled and tried to stop the fight but the suspect then turned and ran out of the bar. I didn't recognize either man and have no idea what the fight was about. The police came but the victim was already dead."
  );

  const [highlightList, setHighlightList] = useState(["mark", "Wilson", "Ressles's"]);

  return (
      <div className="App">
        {highlightWords(paragraph, highlightList)}
      </div>
  );

}

export default App;

