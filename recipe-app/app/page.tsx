"use client";
import React, { useState, useRef } from "react";
import { Coffee, Search, User, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import TagInput from "@/components/tag";
import Loading from "@/components/loading";
import { useRouter } from "next/navigation";
import Navbar from "@/components/navbar";

// Enum for loading states
enum LoadingState {
  IDLE,
  LOADING,
  SUCCESS,
  ERROR
}

export default function Home() {
  const router = useRouter();
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [ingredientInput, setIngredientInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [loadingState, setLoadingState] = useState<LoadingState>(LoadingState.IDLE);
  const searchSectionRef = useRef<HTMLElement>(null);

  const scrollToSearch = () => {
    searchSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const addIngredient = () => {
    if (ingredientInput && !ingredients.includes(ingredientInput)) {
      setIngredients([...ingredients, ingredientInput]);
      setIngredientInput("");
    }
  };

  const removeIngredient = (ingredient: string) => {
    setIngredients(ingredients.filter((item) => item !== ingredient));
  }

  const getIngredients = async () => {
    setLoadingState(LoadingState.LOADING);
    try {
      const response = await fetch(`http://${process.env.NEXT_PUBLIC_IP_ADDRESS}/api/ingredients`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch ingredients");
      }

      const data = await response.json();
      const ingredients = data.data 
      const ingredientsArray = ingredients.split(",")
      
      console.log(ingredientsArray)
      setIngredients(ingredientsArray);
      setLoadingState(LoadingState.SUCCESS);
    } catch (error) {
      console.error("Error in getIngredients:", error);
      setLoadingState(LoadingState.ERROR);
    } finally {
      setLoadingState(LoadingState.IDLE);
    }
  };

  const submitVector = async () => {
    setLoadingState(LoadingState.LOADING);
    try {
      const params = ingredients.concat(tags);
      const address = `http://${process.env.NEXT_PUBLIC_IP_ADDRESS}/api/recipe`;

      const response = await fetch(address, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ params }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch recipes");
      }

      const recipes = await response.json();
      const encodedRecipes = encodeURIComponent(JSON.stringify(recipes));

      const ids = recipes.data.map((recipe: any) => recipe._id);

      const getUrls = async (ids: any) => {
        const urlResponse = await fetch(`http://${process.env.NEXT_PUBLIC_IP_ADDRESS}/api/getImages`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ ids }),
        });

        if (!urlResponse.ok) {
          throw new Error("Failed to fetch image URLs");
        }

        const data = await urlResponse.json();
        return data.data;
      };

      const urls = await getUrls(ids);
      const encodedUrls = encodeURIComponent(JSON.stringify(urls));

      // Combine both encoded parameters in the URL
      router.push(`/recipes?recipes=${encodedRecipes}&urls=${encodedUrls}`);
    } catch (error) {
      console.error("Error in submitVector:", error);
      setLoadingState(LoadingState.ERROR);
    } finally {
      setLoadingState(LoadingState.IDLE);
    }
  };

  const renderContent = () => {
    switch (loadingState) {
      case LoadingState.LOADING:
        return <Loading />;
      case LoadingState.ERROR:
        return <div>An error occurred</div>;
      case LoadingState.SUCCESS:
      case LoadingState.IDLE:
        return (
          <div className="bg-white min-h-screen font-sans">
            <Navbar />
            
            {/* Hero Section */}
            <section className="relative bg-cover bg-center h-screen flex items-center justify-center" style={{backgroundImage: "url('https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&q=80&w=1920&h=1080')"}}>              <div className="absolute inset-0 bg-black opacity-50"></div>
              <div className="relative z-10 text-center text-white">
                <h1 className="text-6xl font-bold mb-4">Chef Quackles</h1>
                <p className="text-2xl mb-8">Discover duckalicious recipes with your favorite ingredients!</p>
                <Button 
                  onClick={scrollToSearch}
                  className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-full text-lg transition duration-300"
                >
                  Start Exploring
                </Button>
              </div>
            </section>

            {/* Search Section */}
      <section ref={searchSectionRef} id="search-section" className="container mx-auto px-4 py-16 bg-gray-50">
        <h2 className="text-4xl font-bold text-center text-green-700 mb-12">Find Your Perfect Recipe</h2>
        
        <div className="grid md:grid-cols-2 gap-8">
          <Card className="bg-white shadow-lg rounded-lg overflow-hidden">
            <CardHeader className="bg-green-100 p-4">
              <CardTitle className="text-2xl font-semibold text-green-700">Search by Ingredients</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  addIngredient();
                }}
                className="space-y-4"
              >
                <Input
                  type="text"
                  value={ingredientInput}
                  onChange={(e) => setIngredientInput(e.target.value)}
                  placeholder="Enter an ingredient"
                  className="w-full p-3 border border-gray-300 rounded-lg"
                />
                <Button
                  type="submit"
                  className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg"
                >
                  Add Ingredient
                </Button>
              </form>
              <div className="mt-4">
                <h3 className="font-semibold mb-2">Added Ingredients:</h3>
                <div className="flex flex-wrap gap-2">
                  {ingredients.map((ingredient, index) => (
                    <span
                      key={index}
                      className="bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded-full flex items-center"
                    >
                      {ingredient}
                      <button
                        onClick={() => removeIngredient(ingredient)}
                        className="ml-1 focus:outline-none"
                      >
                        <X size={14} />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
              <Button
                onClick={getIngredients}
                className="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg"
              >
                Get Ingredients
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg rounded-lg overflow-hidden">
            <CardHeader className="bg-green-100 p-4">
              <CardTitle className="text-2xl font-semibold text-green-700">Search by Tags</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <TagInput tags={tags} setTags={setTags} />
            </CardContent>
          </Card>
        </div>

        <div className="mt-12 flex justify-center">
          <Button
            onClick={submitVector}
            className="
              bg-green-500 text-white
              hover:bg-green-600
              transition-all duration-300 ease-in-out
              transform hover:scale-105 active:scale-95
              shadow-md hover:shadow-lg
              flex items-center justify-center
              px-8 py-4 rounded-full text-lg
              group
            "
          >
            <Search className="mr-2 h-5 w-5 transition-all duration-300 group-hover:h-6 group-hover:w-6" />
            <span className="font-semibold">Search Recipes</span>
          </Button>
        </div>
      </section>
    </div>
    )}
  };

  return renderContent();
}