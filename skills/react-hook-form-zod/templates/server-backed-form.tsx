import { useId } from 'react'
import { useForm, useFormState, useWatch } from 'react-hook-form'
import type { Control } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

export const recordSchema = z.object({
  name: z.string().trim().min(1, 'Name is required'),
  seats: z.string().trim().min(1, 'Seats are required')
    .transform(Number).pipe(z.number().finite().int().min(1)),
})
type Input = z.input<typeof recordSchema>
type Output = z.output<typeof recordSchema>
export type SavedRecord = Output & { id: string }

const emptyValues: Input = { name: '', seats: '' }
const toInput = (record: SavedRecord): Input => ({
  name: record.name,
  seats: String(record.seats),
})

function SeatPreview({ control }: { control: Control<Input, unknown, Output> }) {
  const seats = useWatch({ control, name: 'seats' })
  return <p>Seats: {seats || 'Not set'}</p>
}

// Mount with key={record.id} when editing a different record.
export function ServerBackedForm({
  record, save,
}: {
  record: SavedRecord
  save: (values: Output) => Promise<SavedRecord>
}) {
  const formId = useId()
  const { register, control, handleSubmit, reset, setError } = useForm<Input, unknown, Output>({
    resolver: zodResolver(recordSchema),
    defaultValues: emptyValues,
    values: toInput(record),
    resetOptions: { keepDirtyValues: true },
  })
  const { errors, isSubmitting, isDirty, dirtyFields } = useFormState({ control })
  const hasEdits = isDirty || Object.keys(dirtyFields).length > 0

  return (
    <form id={formId} onSubmit={handleSubmit(async (values) => {
      try {
        const persisted = await save(values)
        reset(toInput(persisted), {
          keepDirtyValues: false,
          keepDefaultValues: false,
          keepDirty: false,
        })
      } catch {
        setError('root.server', { message: 'Save failed. Please try again.' })
      }
    })}>
      <label htmlFor={formId + '-name'}>Name</label>
      <input id={formId + '-name'} {...register('name')} />
      {errors.name && <p>{errors.name.message}</p>}
      <label htmlFor={formId + '-seats'}>Seats</label>
      <input id={formId + '-seats'} type="text" inputMode="numeric" {...register('seats')} />
      {errors.seats && <p>{errors.seats.message}</p>}
      <SeatPreview control={control} />
      {errors.root?.server && <p>{errors.root.server.message}</p>}
      <button type="button" onClick={() => reset(undefined, {
        keepDirtyValues: false,
        keepDirty: false,
      })} disabled={isSubmitting}>Cancel</button>
      <button type="submit" disabled={isSubmitting || !hasEdits}>
        {isSubmitting ? 'Saving…' : 'Save changes'}
      </button>
    </form>
  )
}
