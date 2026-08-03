interface Props {
    children: React.ReactNode;
    className?: string;
}


export default function Card({
    children,
    className = ""
}: Props) {

    return (
        <div className={`bg-white border rounded-xl shadow-sm p-6 ${className}`}>
            {children}
        </div>
    );
}