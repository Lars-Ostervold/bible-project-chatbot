import React from 'react';
import Image from 'next/image';

interface Source {
  file_name: string;
  link: string;
  title: string;
  type_of_media: string;
  thumbnail_url: string;
}
type Sources = Source[];

export const SourceBlocks = ({ sources }: { sources: Sources }) => {
    if (!Array.isArray(sources) || sources.length === 0) {
        return null;
      }
    

    return (
        <div className="mx-auto sm:max-w-2xl sm:px-4">
            <p className="prose prose-neutral dark:text-white mb-1 animate-swoop-in">
                Here are some of the sources I used to answer your question:
            </p>
            <div className = "mb-4 grid grid-cols-1 sm:grid-cols-2 gap-1 sm:gap-2 px-0">
            {sources.map((source, index) => (
                <a href={source.link} key={index} target="_blank" rel="noopener noreferrer">
                    <div className="cursor-pointer rounded-lg border bg-white p-2 hover:bg-zinc-50 dark:bg-zinc-950 dark:hover:bg-zinc-900 animate-swoop-in flex">
                        <div className="w-1/3 relative rounded-lg overflow-hidden">
                            <Image src={source.thumbnail_url} alt="Thumbnail" layout="fill" objectFit="cover"/>
                        </div>
                        <div className="ml-6 flex flex-col justify-center">
                            <h2>{source.title}</h2>
                            <p className="italic text-sm dark:text-white">
                                {source.type_of_media}
                            </p>
                        </div>
                    </div>
                </a>
            ))}
            </div>
        </div>
      );
}