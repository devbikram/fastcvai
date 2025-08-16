# CV Analyzer Frontend

A modern React/Next.js frontend application for CV analysis and enhancement.

## Features

✅ **File Upload Component** - Supports PDF, DOCX, JPG, PNG formats
✅ **Job Information Input** - Current job title and target job description fields  
✅ **CV Analysis Display** - Shows original CV score and missing skills/experience
✅ **Enhancement Form** - Form to fill in missing information
✅ **Enhanced CV Generation** - Submits missing info to backend for enhanced CV
✅ **Download Functionality** - Download button for enhanced DOCX CV
✅ **Modern UI** - Clean, responsive design with step-by-step process
✅ **TypeScript** - Full TypeScript support for type safety

## Tech Stack

- **Next.js 15** - React framework with App Router
- **React 18** - Functional components with hooks
- **TypeScript** - Type safety and better developer experience
- **Tailwind CSS** - Utility-first CSS framework
- **Modern ES6+** - Latest JavaScript features

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend CV Analyzer API running on http://0.0.0.0:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3001](http://localhost:3001) in your browser.

## API Integration

The frontend integrates with the following backend endpoints:

- `POST http://0.0.0.0:8000/upload-cv` - Upload CV for analysis
- `POST http://0.0.0.0:8000/enhance-cv` - Generate enhanced CV with missing info

## Application Flow

1. **Upload Section** - User uploads CV and provides job details
2. **Analysis Results** - Display original CV score and missing skills  
3. **Missing Info Form** - User fills in missing experience/skills
4. **Enhanced CV** - Shows improved score and download option

## File Structure

```
app/
├── cv-analyzer.tsx    # Main CV analyzer component
├── page.tsx          # Home page that renders CV analyzer
├── layout.tsx        # Root layout
└── globals.css       # Global styles
```

## Component Features

### CVAnalyzer Component

- **State Management** - Uses React hooks for component state
- **Form Handling** - Controlled inputs with validation
- **File Upload** - Drag & drop file input with type validation  
- **API Integration** - Fetch calls to backend endpoints
- **Error Handling** - User-friendly error messages
- **Loading States** - Loading indicators during API calls
- **Responsive Design** - Mobile-friendly layout

### Type Definitions

```typescript
type AnalysisResult = {
  id?: string;
  score: number;
  missingSkills: string[];
};

type EnhancedResult = {
  score: number;
  downloadUrl: string;
};
```

## Customization

The component is highly customizable:

- **Styling** - Modify Tailwind classes for different appearance
- **API Endpoints** - Update endpoints in component for different backend
- **File Types** - Adjust `ALLOWED_TYPES` array for different file support
- **Validation** - Add custom validation logic
- **UI Flow** - Modify sections and steps as needed

## Development

### Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Code Quality

- ESLint configuration for code quality
- TypeScript for type checking
- Prettier formatting (if configured)

## Production Deployment

1. Build the application:
```bash
npm run build
```

2. Start the production server:
```bash
npm start
```

The application will be ready for deployment to platforms like Vercel, Netlify, or any Node.js hosting service.
