'use client'

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { Tag, Clock, Users, ChefHat, Utensils } from 'lucide-react';
import Navbar from '@/components/navbar';

interface Recipe {
  _id: string | number;
  name: string;
  ingredients: string;
  recipe: string;
  tags: string;
  time: number;
  nutrition: string;
}

export default function RecipePage() {
  const params = useParams();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const recipesJson = localStorage.getItem('recipes');
        const urlsJson = localStorage.getItem('urls');


        if (recipesJson && urlsJson) {

          const recipes: Recipe[] = JSON.parse(recipesJson);
          const urls: string[] = JSON.parse(urlsJson);
          
          let foundRecipe; 

          for(let i = 0; i < recipes.length; i++) {
            if (recipes[i]._id == params.id) {
              foundRecipe = recipes[i];
              break;
            }
          }

          
          if (foundRecipe) {
            setRecipe(foundRecipe);
            setImageUrl(urls[recipes.indexOf(foundRecipe)]);
          }
        }
      } catch (error) {
        console.error('Error fetching recipe:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [params.id]);

  
  const capitalizeWords = (str: string): string => {
    return str.replace(/\b\w/g, char => char.toUpperCase());
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-green-500"></div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-2xl text-gray-600">Recipe not found</p>
      </div>
    );
  }

  const nutritionLabels = ["Calories", "Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat"];
  const nutritionList = recipe.nutrition
    .slice(1, -1)
    .split(",")
    .map((item, index) => {
      const label = nutritionLabels[index] || `Nutrition ${index + 1}`;
      const value = item.trim();
      return `${label}: ${value}`;
    });

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8 font-sans">
        <div className="max-w-4xl mx-auto bg-white rounded-xl overflow-hidden shadow-lg">
          <div className="relative h-64 sm:h-80">
            <Image 
              src={imageUrl} 
              alt={recipe.name} 
              layout="fill"
              objectFit="cover"
              className="w-full h-full object-center"
            />
            <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
              <h1 className="text-4xl sm:text-5xl font-bold text-white text-center px-4">
                {capitalizeWords(recipe.name)}
              </h1>
            </div>
          </div>
          <div className="p-8">
            <div className="flex flex-wrap items-center justify-between mb-8 text-sm text-gray-600">
              <div className="flex items-center mb-2 sm:mb-0">
                <Clock className="w-5 h-5 mr-2 text-green-600" />
                <span>{recipe.time} min</span>
              </div>
              <div className="flex items-center mb-2 sm:mb-0">
                <Users className="w-5 h-5 mr-2 text-green-600" />
                <span>4 servings</span>
              </div>
              <div className="flex items-center">
                <Utensils className="w-5 h-5 mr-2 text-green-600" />
                <span>Easy</span>
              </div>
            </div>
            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-4 flex items-center text-gray-700">
                <ChefHat className="w-6 h-6 mr-2 text-green-600" />
                Ingredients
              </h2>
              <ul className="text-gray-600 grid grid-cols-1 sm:grid-cols-2 gap-2">
                {recipe.ingredients
                .slice(1,-1)
                .split(",")
                .map((ingredient, index) => (
                  <li key={index} className="flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    {capitalizeWords(ingredient.trim().slice(1,-1))}
                  </li>
                ))}
              </ul>
            </div>
            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-4 flex items-center text-gray-700">
                <ChefHat className="w-6 h-6 mr-2 text-green-600" />
                Steps
              </h2>
              <ol className="text-gray-600 space-y-4">
                {recipe.recipe
                  .slice(1, -1)
                  .split("'")
                  .filter(step => step.trim() !== '' && step.trim() !== ',')
                  .map((step, index) => (
                    <li key={index} className="flex items-start">
                      <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-green-100 rounded-full mr-3 text-green-600 font-semibold">
                        {index + 1}
                      </span>
                      <span className="mt-1">{capitalizeWords(step)}</span>
                    </li>
                  ))}
              </ol>
            </div>
            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-4 flex items-center text-gray-700">
                <ChefHat className="w-6 h-6 mr-2 text-green-600" />
                Nutrition
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {nutritionList.map((nutrition, index) => (
                  <div key={index} className="bg-green-50 p-3 rounded-lg">
                    <p className="text-green-800 font-medium">{capitalizeWords(nutrition)}</p>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h2 className="text-2xl font-semibold mb-4 text-gray-700">Tags</h2>
              <div className="flex flex-wrap gap-2">
                {recipe.tags
                .slice(1, -1)
                .split(',')
                .map((tag, index) => (
                  <span
                    key={index}
                    className="bg-green-100 text-green-800 text-xs font-medium px-3 py-1 rounded-full"
                  >
                    {capitalizeWords(tag.trim().slice(1, -1))}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}