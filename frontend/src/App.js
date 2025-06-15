import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [breeds, setBreeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBreed, setSelectedBreed] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredBreeds, setFilteredBreeds] = useState([]);
  const [filterSize, setFilterSize] = useState("all");
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchBreeds();
  }, []);

  useEffect(() => {
    filterBreeds();
  }, [breeds, searchTerm, filterSize]);

  const fetchBreeds = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/breeds`);
      setBreeds(response.data);
    } catch (error) {
      console.error("Error fetching breeds:", error);
      // Try to populate breeds if empty
      try {
        await axios.post(`${API}/breeds/populate`);
        const response = await axios.get(`${API}/breeds`);
        setBreeds(response.data);
      } catch (populateError) {
        console.error("Error populating breeds:", populateError);
      }
    } finally {
      setLoading(false);
    }
  };

  const filterBreeds = () => {
    let filtered = breeds;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(breed =>
        breed.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        breed.temperament.toLowerCase().includes(searchTerm.toLowerCase()) ||
        breed.breed_group.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by size
    if (filterSize !== "all") {
      filtered = filtered.filter(breed =>
        breed.size.toLowerCase() === filterSize.toLowerCase()
      );
    }

    setFilteredBreeds(filtered);
  };

  const openModal = (breed) => {
    setSelectedBreed(breed);
    setShowModal(true);
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedBreed(null);
    document.body.style.overflow = 'unset';
  };

  const getSizeColor = (size) => {
    switch (size.toLowerCase()) {
      case 'small': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-blue-100 text-blue-800';
      case 'large': return 'bg-orange-100 text-orange-800';
      case 'giant': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCareColor = (level) => {
    switch (level.toLowerCase()) {
      case 'low': return 'bg-green-500';
      case 'moderate': return 'bg-yellow-500';
      case 'high': return 'bg-orange-500';
      case 'very high': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-xl text-gray-600 animate-pulse">Loading amazing dog breeds...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fade-in-up">
              🐕 Dog Breeds Explorer
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90 animate-fade-in-up animation-delay-200">
              Discover Amazing Dog Breeds from Around the World
            </p>
            <div className="flex justify-center animate-fade-in-up animation-delay-400">
              <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-full px-6 py-3">
                <span className="text-lg font-semibold">{breeds.length}+ Breeds Available</span>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-blue-50 to-transparent"></div>
      </header>

      {/* Search and Filter Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8 animate-slide-up">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search by name, temperament, or breed group..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:outline-none transition-colors duration-200"
              />
            </div>
            <div className="md:w-48">
              <select
                value={filterSize}
                onChange={(e) => setFilterSize(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:outline-none transition-colors duration-200"
              >
                <option value="all">All Sizes</option>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
                <option value="giant">Giant</option>
              </select>
            </div>
          </div>
          <div className="mt-4 text-center">
            <p className="text-gray-600">
              Showing {filteredBreeds.length} of {breeds.length} breeds
            </p>
          </div>
        </div>
      </section>

      {/* Breeds Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredBreeds.map((breed, index) => (
            <div
              key={breed.id}
              className="bg-white rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-2xl animate-fade-in-up cursor-pointer group"
              style={{ animationDelay: `${index * 50}ms` }}
              onClick={() => openModal(breed)}
            >
              <div className="relative overflow-hidden h-48">
                <img
                  src={breed.image_url}
                  alt={breed.name}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                  onError={(e) => {
                    e.target.src = 'https://images.unsplash.com/photo-1558788353-f76d92427f16';
                  }}
                />
                <div className="absolute top-3 left-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getSizeColor(breed.size)}`}>
                    {breed.size}
                  </span>
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </div>
              
              <div className="p-5">
                <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-indigo-600 transition-colors duration-200">
                  {breed.name}
                </h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {breed.temperament}
                </p>
                
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Origin:</span>
                    <span className="font-medium text-gray-700">{breed.origin}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Lifespan:</span>
                    <span className="font-medium text-gray-700">{breed.lifespan}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-500">Care Level:</span>
                    <div className="flex items-center space-x-1">
                      <div className={`w-2 h-2 rounded-full ${getCareColor(breed.care_level)}`}></div>
                      <span className="font-medium text-gray-700">{breed.care_level}</span>
                    </div>
                  </div>
                </div>
                
                <button className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-2 px-4 rounded-lg font-semibold transition-all duration-200 hover:from-indigo-600 hover:to-purple-700 transform hover:scale-105 active:scale-95">
                  Learn More
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {filteredBreeds.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold text-gray-700 mb-2">No breeds found</h3>
            <p className="text-gray-500">Try adjusting your search terms or filters</p>
          </div>
        )}
      </section>

      {/* Modal */}
      {showModal && selectedBreed && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-slide-up">
            <div className="relative">
              <button
                onClick={closeModal}
                className="absolute top-4 right-4 z-10 bg-black bg-opacity-50 text-white rounded-full w-10 h-10 flex items-center justify-center hover:bg-opacity-70 transition-all duration-200"
              >
                ✕
              </button>
              
              <div className="relative h-64 md:h-80 overflow-hidden rounded-t-2xl">
                <img
                  src={selectedBreed.image_url}
                  alt={selectedBreed.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://images.unsplash.com/photo-1558788353-f76d92427f16';
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
                <div className="absolute bottom-4 left-4 text-white">
                  <h2 className="text-3xl md:text-4xl font-bold mb-2">{selectedBreed.name}</h2>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSizeColor(selectedBreed.size)}`}>
                    {selectedBreed.size}
                  </span>
                </div>
              </div>
              
              <div className="p-6 md:p-8">
                <div className="mb-6">
                  <p className="text-gray-700 text-lg leading-relaxed">{selectedBreed.description}</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="space-y-4">
                    <h4 className="text-xl font-bold text-gray-800 border-b-2 border-indigo-200 pb-2">
                      Basic Information
                    </h4>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Breed Group:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.breed_group}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Origin:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.origin}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Lifespan:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.lifespan}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Weight:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.weight}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Height:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.height}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h4 className="text-xl font-bold text-gray-800 border-b-2 border-indigo-200 pb-2">
                      Care & Temperament
                    </h4>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Temperament:</span>
                        <span className="font-semibold text-gray-800 text-right">{selectedBreed.temperament}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Care Level:</span>
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${getCareColor(selectedBreed.care_level)}`}></div>
                          <span className="font-semibold text-gray-800">{selectedBreed.care_level}</span>
                        </div>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Exercise Needs:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.exercise_needs}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Grooming Needs:</span>
                        <span className="font-semibold text-gray-800">{selectedBreed.grooming_needs}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Good with Kids:</span>
                        <span className={`font-semibold ${selectedBreed.good_with_kids ? 'text-green-600' : 'text-red-600'}`}>
                          {selectedBreed.good_with_kids ? '✓ Yes' : '✗ No'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Good with Pets:</span>
                        <span className={`font-semibold ${selectedBreed.good_with_pets ? 'text-green-600' : 'text-red-600'}`}>
                          {selectedBreed.good_with_pets ? '✓ Yes' : '✗ No'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {selectedBreed.health_issues && selectedBreed.health_issues.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-xl font-bold text-gray-800 border-b-2 border-indigo-200 pb-2 mb-4">
                      Common Health Issues
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedBreed.health_issues.map((issue, index) => (
                        <span
                          key={index}
                          className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {issue}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;