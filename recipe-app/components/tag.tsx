import React, { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { X } from 'lucide-react';

const predefinedTags = [
  'healthy', 'snacks', 'easy', 'quick', 'breakfast', 'lunch', 'dinner', 'desserts', 'vegetarian', 'vegan',
  'gluten-free', 'low-calorie', 'low-fat', 'low-carb', 'kid-friendly', 'holiday-event', 'party',
  'summer', 'winter', 'fall', 'spring', 'main-dish', 'side-dish', 'appetizers', 'beverages', 'soups', 'stews',
  'salads', 'grilling', 'baking', 'meat', 'chocolate', 'fruits', 'vegetables', 'whole-grains', 'spicy', 'sweet',
  'savory', 'comfort-food', 'no-cook', 'slow-cooker', 'pressure-cooker', 'one-pot', 'stir-fry', 'casseroles',
  'sandwiches', 'burgers', 'pizzas', 'salmon', 'shrimp', 'tofu', 'tempeh', 'quinoa', 'couscous', 'polenta', 'pancakes',
  'waffles', 'smoothies', 'juices', 'bars', 'brownies', 'cupcakes', 'ice-cream',
  'popsicles', 'granola', 'trail-mix', 'sauces', 'dips', 'marinades', 'dressings', 'salsas', 'chutneys', 'jams', 'jellies',
  'spreads', 'condiments', 'herbs', 'spices', 'oils', 'vinegars', 'broths', 'stocks', 'miso', 'fermented', 'pickled',
  'Italian',    'Chinese',   'Mexican',   'Indian',   'French',   'Japanese',   'Thai',   'Greek', 'Spanish',   'Middle Eastern'
];
const TagInput = ({ tags, setTags }: any) => {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>(predefinedTags.slice(0,15));

  const handleInputChange = (e: any) => {
    const value = e.target.value;
    setInput(value);
    const filteredSuggestions = predefinedTags.filter(tag =>
      tag.toLowerCase().includes(value.toLowerCase()) && !tags.includes(tag)
    );
    setSuggestions(filteredSuggestions.slice(0, 15));
  };

  const addTag = (tag: any) => {
    if (tag && !tags.includes(tag)) {
      setTags([...tags, tag]);
      setInput('');
      setSuggestions([]);
    }
  };

  const removeTag = (tagToRemove: any) => {
    setTags(tags.filter((tag:any) => tag !== tagToRemove));
  };

  return (
    <div className="space-y-2">
      <div className="flex space-x-2">
        <Input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type to search tags"
          className="flex-grow"
        />
        <Button onClick={() => addTag(input)} disabled={!input || tags.includes(input)}>
          Add
        </Button>
      </div>
      {suggestions.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {suggestions.map(tag => (
            <Button key={tag} variant="outline" size="sm" onClick={() => addTag(tag)}>
              {tag}
            </Button>
          ))}
        </div>
      )}
      <div className="flex flex-wrap gap-2 mt-2">
        {tags.map( (tag: any) => (
          <span key={tag} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full flex items-center">
            {tag}
            <button onClick={() => removeTag(tag)} className="ml-1 focus:outline-none">
              <X size={14} />
            </button>
          </span>
        ))}
      </div>
    </div>
  );
};

export default TagInput;