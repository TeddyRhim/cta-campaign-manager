interface Props {
    message: string;
}


export default function EmptyState({
    message
}: Props) {

    return (
        <div className="bg-white border rounded-xl p-8 text-center text-gray-500">
            {message}
        </div>
    );
}