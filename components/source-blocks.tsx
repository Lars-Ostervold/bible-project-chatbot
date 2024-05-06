import React from 'react';

export const SourceBlocks = ({ sources }) => {
    if (!Array.isArray(sources) || sources.length === 0) {
        return null;
      }
    
    return (
        <div className="mx-auto sm:max-w-2xl sm:px-4">
            <p className="prose prose-neutral dark:text-white mb-1 animate-swoop-in">
                Here are the sources I used to answer your question:
            </p>
            <div className = "mb-4 grid grid-cols-2 gap-2 px-4 sm:px-0">
            {sources.map((source, index) => (
                <div key={index} className="`cursor-pointer rounded-lg border bg-white p-4 hover:bg-zinc-50 dark:bg-zinc-950 dark:hover:bg-zinc-900 animate-swoop-in">
                <h2>{source.title}</h2>
                <a href={source.link}>Link</a>
                </div>
            ))}
            </div>
        </div>
      );
}