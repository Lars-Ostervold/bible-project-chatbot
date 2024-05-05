import React from 'react';

export const SourceBlocks = ({ sources }) => {
    return (
        <div>
          <h1>Sources</h1>
          {sources.map((source, index) => (
            <div key={index} className="card bg-white dark:bg-gray-900 text-black dark:text-white rounded-lg shadow-md p-4 md:pd-2 border border-gray-400 dark:border-gray-600 overflow-hidden transform transition-transform duration-200 ease-in-out hover:scale-105">
              <h2>{source.title}</h2>
              <a href={source.link}>Link</a>
            </div>
          ))}
        </div>
      );
}