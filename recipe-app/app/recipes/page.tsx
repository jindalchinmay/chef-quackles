"use client"
import React from 'react';
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Navbar from '@/components/navbar';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

type Recipe = {
  _id: string;
  name: string;
  ingredients: string;
  recipe: string;
  tags: string;
  steps: string[];
  time: number;
  nutrition: string;
};

export default function Results() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [imageUrls, setImageUrls] = useState<{[key: string]: string}>({});
  const [sortOption, setSortOption] = useState<string>("default");
  const [originalRecipes, setOriginalRecipes] = useState<Recipe[]>([]);

  function capitalizeAfterSpace(str: string) {
    return str.replace(/\b\w/g, (char) => char.toUpperCase());
  }

  useEffect(() => {
    const recipesParam = searchParams.get("recipes");
    const urlParam = searchParams.get("urls");
 
    if (recipesParam && urlParam) {
      const decodedRecipes = JSON.parse(decodeURIComponent(recipesParam));
      const decodedUrls = JSON.parse(decodeURIComponent(urlParam));
      
      setRecipes(decodedRecipes.data);
      setOriginalRecipes(decodedRecipes.data);

      console.log(decodedRecipes.data.map((r: Recipe) => r._id));

      const urlMap: {[key: string]: string} = {};
      decodedRecipes.data.forEach((recipe: Recipe, index: number) => {
        urlMap[recipe._id] = decodedUrls[index];
      });
      setImageUrls(urlMap);

      localStorage.setItem("recipes", JSON.stringify(decodedRecipes.data));
      localStorage.setItem("urls", JSON.stringify(decodedUrls));
    }
  }, [searchParams]);

  const getCalories = (nutrition: string): number => {
    const calorieString = nutrition.split(',')[0].slice(1);
    return parseInt(calorieString) || 0;
  };

  const sortRecipes = () => {
    let sortedRecipes = [...recipes];
    switch (sortOption) {
      case "time":
        sortedRecipes.sort((a, b) => a.time - b.time);
        break;
      case "calories":
        sortedRecipes.sort((a, b) => {
          const caloriesA = getCalories(a.nutrition);
          const caloriesB = getCalories(b.nutrition);
          return caloriesA - caloriesB;
        });
        break;
      default:
        sortedRecipes = [...originalRecipes];
        break;
    }
    setRecipes(sortedRecipes);
  };

  const handleSortOptionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOption(event.target.value);
  };

  return (
    <>
    <Navbar />
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <h1 className="text-4xl font-extrabold mb-8 text-center text-green-700">Delicious Recipes</h1>
      
      <div className="mb-6 flex justify-end items-center space-x-2">
        <select 
          className="p-2 border rounded-md"
          onChange={handleSortOptionChange}
          value={sortOption}
        >
          <option value="default">Default</option>
          <option value="time">Time</option>
          <option value="calories">Calories</option>
        </select>
        <button 
          onClick={sortRecipes}
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
        >
          Sort
        </button>
      </div>

      {recipes.length === 0 ? (
        <p className="text-center text-gray-600">No recipes found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {recipes.map((recipe: Recipe) => (
            <div key={recipe._id} className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
              <Image src={imageUrls[recipe._id]} alt={recipe.name} width={400} height={300} />
              <div className="p-6">
                <Link href={`/recipes/${recipe._id}`}>
                  <h2 className="text-2xl font-bold text-center text-gray-800 mb-2 py-2 hover:text-green-600 transition-colors duration-300">
                    {capitalizeAfterSpace(recipe.name)}
                  </h2>
                </Link>
                <div className="flex items-center justify-between mb-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <span>⏱️ {recipe.time} min</span>
                  </div>
                  <div className="flex items-center">
                    <span>🔥 {recipe.nutrition.split(',')[0].slice(1)} cal</span>
                  </div>
                </div>
                <div className="mb-4">
                  <h3 className="text-lg font-semibold mb-2 flex items-center text-gray-700">
                    👨‍🍳 Ingredients
                  </h3>
                  <ul className="text-sm text-gray-600 list-disc list-inside">
                    {recipe.ingredients
                      .slice(1, -1)
                      .split(",")
                      .map((ingredient: string, index: number) => (
                        <li key={index} className="mb-1">{capitalizeAfterSpace(ingredient.trim().slice(1, -1))}</li>
                      ))}
                  </ul>
                </div>
                <div className="flex flex-wrap gap-2">
                  {recipe.tags
                    .slice(1, -1)
                    .split(",")
                    .map((tag: string) => (
                      <span
                        key={tag}
                        className="bg-green-100 text-green-800 text-xs font-medium px-3 py-1 rounded-full"
                      >
                        {capitalizeAfterSpace(tag.trim().slice(1, -1))}
                      </span>
                    ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
    </>
  );
}