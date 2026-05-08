import { Routes, Route, NavLink, Navigate, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import CategoriasCRUD from './pages/CategoriasCRUD'
import IngredientesCRUD from './pages/IngredientesCRUD'
import ProductosCRUD from './pages/ProductosCRUD'
import Login from './pages/Login'

function App() {
  const [userRole, setUserRole] = useState<'admin' | 'guest' | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Migrar vieja autenticación si existe
    if (localStorage.getItem('isAuthenticated') === 'true' && !localStorage.getItem('userRole')) {
      localStorage.setItem('userRole', 'admin')
      localStorage.removeItem('isAuthenticated')
    }
    
    const role = localStorage.getItem('userRole') as 'admin' | 'guest' | null
    if (role) {
      setUserRole(role)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('userRole')
    setUserRole(null)
    navigate('/login')
  }

  if (!userRole) {
    return (
      <Routes>
        <Route path="/login" element={<Login onLogin={(role) => setUserRole(role)} />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  const isAdmin = userRole === 'admin'

  const navItems = isAdmin 
    ? [
        { to: '/categorias', label: 'Categorías' },
        { to: '/ingredientes', label: 'Ingredientes' },
        { to: '/productos', label: 'Productos' },
      ]
    : [
        { to: '/productos', label: 'Menú' }
      ]

  return (
    <div className="min-h-screen bg-white">
      <nav className="bg-gray-800 text-white px-4 py-3 flex justify-between items-center">
        <div className="flex gap-4 items-center">
          <span className="font-bold mr-4">{isAdmin ? 'Catálogo de Productos' : 'Menú'}</span>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `px-3 py-1 rounded ${isActive ? 'bg-gray-600' : 'hover:bg-gray-700'}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
        <button 
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm transition-colors cursor-pointer"
        >
          Cerrar Sesión
        </button>
      </nav>

      <main>
        <Routes>
          {isAdmin ? (
            <>
              <Route path="/" element={<Navigate to="/categorias" replace />} />
              <Route path="/categorias" element={<CategoriasCRUD />} />
              <Route path="/ingredientes" element={<IngredientesCRUD />} />
              <Route path="/productos" element={<ProductosCRUD />} />
              <Route path="*" element={<Navigate to="/categorias" replace />} />
            </>
          ) : (
            <>
              <Route path="/" element={<Navigate to="/productos" replace />} />
              <Route path="/productos" element={<ProductosCRUD readOnly={true} />} />
              <Route path="*" element={<Navigate to="/productos" replace />} />
            </>
          )}
        </Routes>
      </main>
    </div>
  )
}

export default App
