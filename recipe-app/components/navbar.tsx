import Link from "next/link";
import { Home, Menu } from "lucide-react";
import Image from 'next/image';

const Logo = () => (
  <div className="relative w-8 h-8 mr-2 overflow-hidden rounded-full">
  <Image
    src="/logochefquackles.png"
    alt="Chef Quackles Logo"
    layout="fill"
    objectFit="cover"
  />
</div>
);

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center bg-white shadow-lg px-4 py-3 md:px-8 sticky top-0 z-10">
      <Link className="text-green-600 font-bold text-2xl flex items-center" href="/">
        <span className="mr-2"><Logo /></span> Chef Quackles
      </Link>
      <div className="flex items-center space-x-4">
        <Link className="text-gray-600 hover:text-green-600 transition-colors duration-200 hidden md:inline" href="/">
          Recipes
        </Link>
        <Link className="bg-green-600 text-white px-4 py-2 rounded-full hover:bg-green-700 transition-colors duration-200 flex items-center" href="/">
          <Home className="w-4 h-4 mr-2" />
          <span className="hidden md:inline">Home</span>
        </Link>
        <button className="text-gray-600 md:hidden">
          <Menu className="w-6 h-6" />
        </button>
      </div>
    </nav>
  );
}